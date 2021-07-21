import asyncio
from asyncio import sleep
from random import shuffle

from aiogram.types import ChatActions
from aiogram.utils.exceptions import BadRequest

from bot.controllers import BaseController
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.models.Roles import Roles, get_cap
from bot.models.Roles.Civil import Civil
from bot.models.Roles.Mafia import Mafia
from bot.types import ChatId
from bot.localization import Localization
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

        for user, role in zip(players, roles):
            session.roles[user.id] = role(user, session)

        print(session.roles)  # todo: remove

    @classmethod
    async def greet_roles(cls, session: Session):
        await asyncio.wait([role.greet() for role in session.roles.values()])

    @classmethod
    async def send_roles_actions(cls, session: Session):
        await asyncio.wait([role.send_action() for role in session.roles.values()])

    @classmethod
    async def go_day(cls, session: Session):
        tasks = \
            lambda: asyncio.sleep(session.settings.values['time']['day']),

        for task in tasks:
            if session.status != SessionStatus.game:
                return
            await task()

    @classmethod
    async def go_night(cls, session: Session):
        if session.status != SessionStatus.game:
            return
        asyncio.create_task(async_timeout(session.settings.values['time']['night'], cls.go_day, session))
        for role in session.roles.values():
            role.action = None
        await cls.send_roles_actions(session)

    @classmethod
    async def start_game(cls, session: Session):
        await cls.dp.loop.run_in_executor(None, GameController.attach_roles, session)
        session.status = SessionStatus.game
        await cls.greet_roles(session)
        if session.settings.values['game']['start_at_night']:
            asyncio.create_task(cls.go_night(session))
        else:
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
    async def cancel_registration(cls, chat_id: ChatId, t: Localization):
        SessionController.kill_session(chat_id)
        await MessageController.send_registration_force_stopped(chat_id, t)

    @classmethod
    async def stop_game(cls, chat_id: ChatId, t: Localization):
        SessionController.kill_session(chat_id)
        await MessageController.send_game_force_stopped(chat_id, t)

    @classmethod
    async def force_stop(cls, session: Session):
        t = session.t
        chat_id = session.chat_id

        if session.status == SessionStatus.game:
            await GameController.stop_game(chat_id, t)
        elif session.status == SessionStatus.registration:
            await GameController.cancel_registration(chat_id, t)
        else:
            await MessageController.send_nothing_to_stop(chat_id, t)

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
