import asyncio
from asyncio import sleep

from aiogram.types import ChatActions, Message
from aiogram.utils.exceptions import BadRequest

from bot.controllers import DispatcherProvider
from bot.controllers.ActionController.ActionController import ActionController
from bot.controllers.ActionController.Actions.VoteAction import VoteAction, DayKillVoteAction
from bot.controllers.ActionController.types import VoteFailReason
from bot.controllers.GameController.utils import attach_roles, greet_roles, send_roles_vote, resolve_results, \
    resolve_schedules, run_tasks, show_game_state, send_game_phase, send_roles_actions, promote_roles_if_need, \
    apply_actions, attach_mafia_chat, resolve_failure_votes
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.ReactionCounterController.ReactionCounterController import ReactionCounterController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.localization import Localization
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.models.Roles import BaseRole
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.message import attach_last_words
from bot.utils.restriction import restriction_with_prev_state, SEND_RESTRICTIONS
from bot.utils.shared import is_error, async_timeout, async_wait


class GameController(DispatcherProvider):

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
    async def affect_roles(cls, session: Session, store: dict):
        bot = cls.dp.bot

        async def dead_schedule(role: BaseRole):
            #  todo: add translation
            global_text = f'{role.user.get_mention()} was killed.\n'
            if session.settings.values['game']['show_role_of_dead']:
                global_text += f'They was {role.shortcut}\n'
            if session.settings.values['game']['show_killer']:
                global_text += f'Seems killer was {role.killed_by}'
            await bot.send_message(session.chat_id, global_text)

        async def post_results_schedule(role: BaseRole):
            if session.status != SessionStatus.game:
                return
            if not session.settings.values['game']['last_words']:
                await bot.send_message(role.user.id, 'You were killed')
                return

            async def handler(msg: Message):
                await bot.send_message(session.chat_id, f'Last words of {role.user.get_mention()} was:')
                await msg.copy_to(session.chat_id)

            session.handlers.append(await attach_last_words(
                role.user.id,
                'You were killed, send your last words here',
                handler
            ))

        #  todo: add translation to whole phrases and move to MessageController
        async def apply_effect(user_id, role):
            if session.settings.values['game']['show_private_night_actions']:
                if role.cured:
                    await bot.send_message(user_id, "You were cured by doctor")
                if role.just_checked:
                    await bot.send_message(user_id, "You were checked by commissioner")
                if role.blocked:
                    await bot.send_message(user_id, "You were blocked by whore")
                if role.acquitted:
                    await bot.send_message(user_id, "You were acquitted by lawyer")
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
                    text = f'{role.user.get_mention()} was lynched.'
                    if session.settings.values['game']['show_role_of_dead']:
                        text += f'\nThey was {role.shortcut}'
                    await cls.dp.bot.send_message(session.chat_id, text)
                if session.settings.values['game']['mute_messages_from_dead']:
                    await session.restrict_role(user_id)

        await async_wait([apply_effect(*items) for items in session.roles.items()])

    @classmethod
    async def apply_game_result(cls, session: Session, winner: str):
        if not winner:
            return

        winners = ''
        losers = ''
        for role in session.roles.values():
            line = f'{role.user.get_mention()} is {role.shortcut}\n'
            if not role.alive:
                if role.won:
                    winners += line
                else:
                    losers += line
            else:
                if role.team != winner:
                    losers += line
                else:
                    winners += line

        await MessageController.send_game_results(session.chat_id, session.t, winner, winners, losers)
        cls.stop_game(session)

    @classmethod
    async def resolve_day_lynching(cls, session: Session):
        votes = []
        for role in session.roles.values():
            if isinstance(role.action, VoteAction):
                votes.append(role.action)
            role.action = None

        actions, comments = await ActionController.resole_votes(votes)
        if not actions:
            reason: VoteFailReason = comments.get(DayKillVoteAction)
            await MessageController.send_vote_failure_reason(session.chat_id, session.t, reason)
            return

        action = actions[0]

        if session.settings.values['game']['lynching_confirmation']:
            vote_msg = await ReactionCounterController.send_reaction_counter(
                session.chat_id,
                f'Are you sure you want to lynch {action.target.user.get_mention()}?',  # todo: add localization
                ['👍', '👎'],
                False,
                [role.user.id for role in session.roles.values() if role.alive],
                [action.target.user.id]
            )
            await sleep(session.settings.values['time']['vote'])
            await ReactionCounterController.stop_reaction_counter(reaction_counter=vote_msg)

            if session.status != SessionStatus.game:
                return

            yes_count = len(vote_msg.reactions['👍'])
            no_count = len(vote_msg.reactions['👎'])

            if yes_count == no_count:
                # todo: add translation
                await cls.dp.bot.send_message(session.chat_id, 'The opinions of the townspeople diverged')
                return
            if yes_count < no_count:
                # todo: add translation
                await cls.dp.bot.send_message(
                    session.chat_id,
                    f'The townspeople changed their minds to hang {action.target.user.get_mention()}'
                )
                return

        await action.apply()

    @classmethod
    async def go_day(cls, session: Session):
        cross_pipeline_store = {}
        tasks = \
            lambda: apply_actions(session, cross_pipeline_store), \
            lambda: cls.affect_roles(session, cross_pipeline_store), \
            lambda: resolve_failure_votes(session, cross_pipeline_store['vote_fails_reasons']), \
            lambda: cls.night_restriction(session, False), \
            lambda: resolve_results(session, cross_pipeline_store), \
            lambda: send_game_phase(session, cross_pipeline_store), \
            lambda: resolve_schedules(cross_pipeline_store.get('schedule')), \
            lambda: cls.apply_game_result(session, cross_pipeline_store.get('winner')), \
            lambda: resolve_schedules(cross_pipeline_store.get('post_schedule')), \
            lambda: show_game_state(session, cross_pipeline_store.get('config')), \
            lambda: asyncio.sleep(session.settings.values['time']['day']), \
            lambda: send_roles_vote(session), \
            lambda: asyncio.sleep(session.settings.values['time']['poll']), \
            lambda: cls.resolve_day_lynching(session)

        await run_tasks(session, tasks)
        session.toggle()
        asyncio.create_task(cls.go_night(session))

    @classmethod
    async def go_night(cls, session: Session):

        async def schedule_day():
            await cls.remove_mafia_chat(session)
            session.toggle()
            await cls.go_day(session)

        cross_pipeline_store = {}

        tasks = \
            lambda: cls.affect_roles(session, cross_pipeline_store), \
            lambda: resolve_results(session, cross_pipeline_store), \
            lambda: cls.apply_game_result(session, cross_pipeline_store.get('winner')), \
            lambda: attach_mafia_chat(session), \
            lambda: cls.night_restriction(session), \
            lambda: promote_roles_if_need(session), \
            lambda: MessageController.send_night(session.chat_id, session.t), \
            lambda: show_game_state(session, cross_pipeline_store.get('config')), \
            lambda: send_roles_actions(session)

        asyncio.create_task(async_timeout(session.settings.values['time']['night'], schedule_day))

        await run_tasks(session, tasks)

    @classmethod
    async def night_restriction(cls, session: Session, restrict: bool = True):
        roles = [role for role in session.roles.values() if role.alive]
        if restrict:
            for role in roles:
                session.restrictions[role.user.id] = await restriction_with_prev_state(
                    cls.dp.bot,
                    session.chat_id,
                    role.user.id,
                    SEND_RESTRICTIONS
                )
        else:
            for role in roles:
                await restriction_with_prev_state(
                    cls.dp.bot,
                    session.chat_id,
                    role.user.id,
                    session.restrictions.pop(role.user.id, {'can_send_messages': True})
                )

    @classmethod
    async def remove_mafia_chat(cls, session: Session):
        if not session.mafia_chat_handler:
            return
        try:
            cls.dp.message_handlers.unregister(session.mafia_chat_handler)
        except ValueError:
            pass

    @classmethod
    async def start_game(cls, session: Session):
        await cls.dp.loop.run_in_executor(None, attach_roles, session)
        session.status = SessionStatus.game
        await greet_roles(session)
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
        SessionController.kill_session(session.chat_id)
        for chat_id, restriction in session.restrictions.items():
            asyncio.create_task(restriction_with_prev_state(
                cls.dp.bot,
                session.chat_id,
                chat_id,
                restriction
            ))
        for handler in session.handlers:
            try:
                if handler:
                    cls.dp.message_handlers.unregister(handler)
            except ValueError:
                pass
        if session.mafia_chat_handler:
            try:
                cls.dp.message_handlers.unregister(session.mafia_chat_handler)
            except ValueError:
                pass

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
