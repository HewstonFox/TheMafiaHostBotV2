import asyncio
import datetime
from asyncio import sleep
from pprint import pprint
from random import shuffle
from typing import Optional

from aiogram.types import ChatActions, Message, ChatPermissions
from aiogram.utils.exceptions import BadRequest

from bot.controllers import BaseController
from bot.controllers.ActionController.ActionController import ActionController
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.localization import Localization
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.models.Roles import Roles, get_cap, BaseRole
from bot.models.Roles.Civil import Civil
from bot.models.Roles.Commissioner import Commissioner
from bot.models.Roles.Don import Don
from bot.models.Roles.Mafia import Mafia
from bot.models.Roles.Maniac import Maniac
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team
from bot.types import ChatId, ResultConfig
from bot.utils.game import get_result_config, run_tasks, resolve_schedules
from bot.utils.message import attach_last_words
from bot.utils.shared import is_error, async_timeout


class GameController(BaseController):

    @classmethod
    async def run_new_game(cls, session: Session, timer: int = None):
        await cls.dp.bot.send_chat_action(session.chat_id, ChatActions.TYPING)

        t = session.t
        chat_id = session.chat_id
        try:
            SessionController.push_session(session)
        except SessionAlreadyActiveError:
            if session.status == SessionStatus.registration:
                await MessageController.send_registration_is_already_started(chat_id, t)
            else:
                await MessageController.send_game_is_already_started(chat_id, t)
            return

        to_clean_msg = []

        async def send_connect_message():
            msg = await MessageController.send_registration_start(chat_id, t, ', '.join(
                map(lambda x: x.get_mention(), session.players.values())))
            to_clean_msg.insert(0, msg.message_id)
            await cls.dp.bot.pin_chat_message(chat_id, msg.message_id, True)

        await send_connect_message()

        async def player_subscriber(players):
            await MessageController.update_registration_start(
                chat_id,
                to_clean_msg[0],
                session.t,
                ', '.join(map(lambda x: x.get_mention(), session.players.values()))
            )

        session.players.subscribe(player_subscriber)

        session.timer = timer or session.settings.values['time']['registration']

        session.status = SessionStatus.registration

        while session.timer > 0:
            if session.status != SessionStatus.registration:
                break
            await sleep(1)
            session.timer -= 1
            if not session.timer % 30 and session.timer > 0:
                try:
                    m = await MessageController.send_registration_reminder(chat_id, t, session.timer, to_clean_msg[0])
                    if is_error(m):
                        raise m
                    to_clean_msg.append(m.message_id)
                except BadRequest:
                    await send_connect_message()

            if 0 < session.timer <= 5:
                m = await cls.dp.bot.send_message(chat_id, str(session.timer))  # todo add final countdown
                to_clean_msg.append(m.message_id)

        session.players.unsubscribe(player_subscriber)

        await cls.dp.bot.unpin_chat_message(chat_id, to_clean_msg[0])
        await MessageController.cleanup_messages(chat_id, to_clean_msg)

        if session.status == SessionStatus.registration:
            if len(session.players) < session.settings.values['players']['min']:
                await cls.dp.bot.send_message(chat_id, '*Not enough players to start')
                # todo: move to MessageController add translation
                SessionController.kill_session(chat_id)
                return
            asyncio.create_task(GameController.start_game(session))

    @classmethod
    def attach_roles(cls, session: Session):
        players = session.players.values()
        settings = session.settings.values['roles']
        roles = []
        players_count = len(players)

        for role in [role for role in Roles if
                     role != Civil and (
                             settings[role.shortcut].get('enable') is None or settings[role.shortcut].get('enable'))]:
            _roles = [role] * int(players_count / settings[role.shortcut]['n'] + 0.5)
            if (cap := get_cap(role)) and len(_roles):
                _roles[0] = cap
            roles.extend(_roles)

        roles = sorted(roles, key=lambda x: x != Mafia)
        roles = roles[:players_count]
        if (difference := players_count - len(roles)) > 0:
            roles.extend([Civil] * difference)

        shuffle(roles)

        index = 1
        for user, role in zip(players, roles):
            session.roles[user.id] = role(user, session, index)
            index += 1

        print(session.roles)  # todo: remove

    @classmethod
    async def greet_roles(cls, session: Session):
        await asyncio.wait([role.greet() for role in session.roles.values()])

    @classmethod
    async def affect_roles(cls, session: Session, store: dict):
        bot = cls.dp.bot

        async def dead_schedule(role: BaseRole):
            #  todo: add translation
            global_text = f'{role.user.get_mention()} was killed.\n'
            if session.settings.values['game']['show_role_of_dead']:
                global_text += f'They were {role.shortcut}\n'
            if session.settings.values['game']['show_killer']:
                global_text += f'Seems killer is {role.killed_by}'
            await bot.send_message(session.chat_id, global_text)

        async def post_results_schedule(role: BaseRole):
            if session.status != SessionStatus.game:
                return
            if not session.settings.values['game']['last_words']:
                if session.settings.values['game']['show_private_night_actions']:
                    await bot.send_message(role.user.id, 'You were killed')
                return

            async def handler(msg: Message):
                await bot.send_message(session.chat_id, f'Last words of {role.user.get_mention()} was:')
                await msg.copy_to(session.chat_id)

            session.handlers.append(await attach_last_words(
                cls.dp,
                role.user.id,
                'You were killed, send your last words here',
                handler
            ))

        #  todo: add translation to whole phrases and move to MessageController
        async def apply_effect(user_id, role):
            if session.settings.values['game']['show_private_night_actions']:
                if role.cured:
                    await bot.send_message(user_id, "You was cured by doctor")
                if role.just_checked:
                    await bot.send_message(user_id, "You was checked by commissioner")
                if role.blocked:
                    await bot.send_message(user_id, "You was blocked by whore")
                if role.acquitted:
                    await bot.send_message(user_id, "You was acquitted by lawyer")
            if role.just_killed:
                if role.killed_by != Team.civ:
                    if 'just_dead' not in store:
                        store['just_dead'] = []
                    if 'schedule' not in store:
                        store['schedule'] = []
                    if 'post_schedule' not in store:
                        store['post_schedule'] = []
                    store['just_dead'].append(user_id)
                    store['schedule'].append(lambda: dead_schedule(role))
                    store['post_schedule'].append(lambda: post_results_schedule(role))
                else:
                    await bot.send_message(session.chat_id, f'{role.user.get_mention()} was lynched.')
                await session.restrict_role(user_id)

        await asyncio.wait([apply_effect(*items) for items in session.roles.items()])

    @classmethod
    async def send_roles_vote(cls, session: Session):
        await MessageController.send_vote(session.chat_id, session.t)
        players: list[Incognito] = list(session.roles.values())  # just for typehint
        await asyncio.wait([player.send_vote() for player in players if player.alive])

    @classmethod
    async def get_session_winner(cls, config: dict) -> Optional[str]:
        alive: list[BaseRole] = config['alive']
        if (alive_count := len(alive)) > 2:
            mafia_count = len([mafia for mafia in alive if isinstance(mafia, Mafia)])
            if not mafia_count:
                return Team.civ
            peace_count = alive_count - mafia_count
            if mafia_count >= peace_count:
                return Team.maf
        else:
            danger_roles = Mafia, Don, Maniac
            a, b = alive
            type_a = type(a)
            type_b = type(b)
            is_danger_a = type_a in danger_roles
            is_danger_b = type_b in danger_roles
            if a.team == b.team == Team.civ:
                return a.team
            elif is_danger_a != is_danger_b and Commissioner not in (type_a, type_b):
                return a.team if is_danger_a else b.team
            return Mafia.team if a.team == b.team == Team.maf else Team.BOTH

    @classmethod
    async def show_game_state(cls, session: Session, config: Optional[ResultConfig]):
        if not config:
            return
        await MessageController.send_game_results(
            session.chat_id,
            session.t,
            config,
            session.settings.values['game']['show_live_roles']
        )

    @classmethod
    async def resolve_results(cls, session: Session, store: dict):
        result_config = get_result_config(session)
        winner = await cls.get_session_winner(result_config)
        if not winner:
            store['config'] = result_config
            return
        # todo: add translation and move to MessageController
        await session.bot.send_message(session.chat_id, f'winner is {winner}')
        cls.stop_game(session)

    @classmethod
    async def send_roles_actions(cls, session: Session):
        await asyncio.wait([role.send_action() for role in session.roles.values() if role.alive])

    @classmethod
    async def go_day(cls, session: Session):
        cross_pipeline_store = {}
        tasks = \
            lambda: ActionController.apply_actions(session.roles), \
            lambda: cls.affect_roles(session, cross_pipeline_store), \
            lambda: MessageController.send_day(
                session.chat_id, session.t, session.day_count,
                bool(cross_pipeline_store.get('just_dead'))
            ), \
            lambda: resolve_schedules(cross_pipeline_store.get('schedule')), \
            lambda: cls.resolve_results(session, cross_pipeline_store), \
            lambda: resolve_schedules(cross_pipeline_store.get('post_schedule')), \
            lambda: cls.show_game_state(session, cross_pipeline_store.get('config')), \
            lambda: asyncio.sleep(session.settings.values['time']['day']), \
            lambda: cls.send_roles_vote(session), \
            lambda: asyncio.sleep(session.settings.values['time']['vote'])

        await run_tasks(session, tasks)
        session.toggle()
        asyncio.create_task(cls.go_night(session))

    @classmethod
    async def go_night(cls, session: Session):

        async def schedule_day():
            session.toggle()
            await cls.go_day(session)

        cross_pipeline_store = {}

        tasks = \
            lambda: ActionController.apply_actions(session.roles), \
            lambda: cls.affect_roles(session, cross_pipeline_store), \
            lambda: cls.resolve_results(session, cross_pipeline_store), \
            lambda: MessageController.send_night(session.chat_id, session.t), \
            lambda: cls.show_game_state(session, cross_pipeline_store.get('config')), \
            lambda: cls.send_roles_actions(session)

        asyncio.create_task(async_timeout(session.settings.values['time']['night'], schedule_day))

        await run_tasks(session, tasks)

    @classmethod
    async def start_game(cls, session: Session):
        await cls.dp.loop.run_in_executor(None, GameController.attach_roles, session)
        session.status = SessionStatus.game
        await cls.greet_roles(session)
        if session.is_night:
            asyncio.create_task(cls.go_night(session))
        else:
            session.day_count += 1
            asyncio.create_task(cls.go_day(session))

    @classmethod
    async def skip_registration(cls, chat_id: ChatId, t: Localization):
        session = SessionController.get_session(chat_id)
        if len(session.players) < session.settings.values['players']['min']:
            await cls.dp.bot.send_message(chat_id, '*Not enough players to start')
            # todo: move to MessageController add translation
            return
        session.timer = -1
        await MessageController.send_registration_skipped(chat_id, t)

    @classmethod
    def stop_game(cls, session: Session):
        for handler in session.handlers:
            try:
                cls.dp.message_handlers.unregister(handler)
            except ValueError:
                pass

        SessionController.kill_session(session.chat_id)

    @classmethod
    async def force_stop(cls, session: Session):
        t = session.t
        chat_id = session.chat_id

        session_status = session.status

        if session_status == SessionStatus.pending:
            await MessageController.send_nothing_to_stop(chat_id, t)
            return

        GameController.stop_game(session)

        if session_status == SessionStatus.game:
            await MessageController.send_game_force_stopped(chat_id, t)
        elif session_status == SessionStatus.registration:
            await MessageController.send_registration_force_stopped(chat_id, t)

    @classmethod
    async def force_start(cls, session: Session):
        t = session.t
        chat_id = session.chat_id
        if session.status != SessionStatus.registration:
            await MessageController.send_nothing_to_skip(chat_id, t)
            return

        await GameController.skip_registration(chat_id, t)

    @classmethod
    async def change_registration_time(cls, session: Session, time: int, sign: int):
        chat_id = session.chat_id
        t = session.t
        if session.status != SessionStatus.registration:
            if sign:
                await MessageController.send_nothing_to_extend(chat_id, t)
            else:
                await MessageController.send_nothing_to_reduce(chat_id, t)
            return

        session.timer += time * sign

        if sign >= 0:
            await MessageController.send_registration_extended(chat_id, t, time, session.timer)
        else:
            await MessageController.send_registration_reduced(chat_id, t, time, session.timer)
