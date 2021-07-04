from asyncio import sleep

from aiogram import Dispatcher
from aiogram.types import ChatActions
from aiogram.utils.exceptions import MessageToReplyNotFound

from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.types import ChatId
from bot.localization import Localization
from bot.utils.shared import is_error


class GameController:
    dp: Dispatcher

    @classmethod
    async def run_new_game(cls, session: Session, time: int = None):
        await cls.dp.bot.send_chat_action(session.chat_id, ChatActions.TYPING)

        t = session.t
        chat_id = session.chat_id
        try:
            SessionController.push_session(session)
        except SessionAlreadyActiveError:
            await MessageController.send_registration_is_already_started(chat_id, t)
            return

        msg = await MessageController.send_registration_start(chat_id, t)

        async def player_subscriber(players):
            await MessageController.update_registration_start(chat_id, msg.message_id, session)

        session.players.subscribe(player_subscriber)

        session.timer = time or 60 * 1
        to_clean_msg = [msg.message_id]

        session.status = SessionStatus.registration

        while session.timer:
            if session.status != SessionStatus.registration:
                break
            await sleep(1)
            session.timer -= 1
            if not session.timer % 10 and session.timer > 0:
                try:
                    m = await MessageController.send_registration_reminder(chat_id, t, session.timer, to_clean_msg[0])
                    if is_error(m):
                        raise m
                except MessageToReplyNotFound:
                    m = await MessageController.send_registration_start(chat_id, t, session)
                to_clean_msg.append(m.message_id)

            if 0 < session.timer <= 5:
                m = await cls.dp.bot.send_message(chat_id, str(session.timer))  # todo add final countdown
                to_clean_msg.append(m.message_id)

        session.players.unsubscribe(player_subscriber)

        await MessageController.cleanup_messages(chat_id, to_clean_msg)

        if session.status == SessionStatus.registration:
            session.status = SessionStatus.game

    @classmethod
    async def skip_registration(cls, chat_id: ChatId, t: Localization):
        session = SessionController.get_session(chat_id)
        session.status = SessionStatus.game
        await MessageController.send_registration_skipped(chat_id, t)

    @classmethod
    async def cancel_registration(cls, chat_id: ChatId, t: Localization):
        SessionController.kill_session(chat_id)
        await MessageController.send_registration_force_stopped(chat_id, t)

    @classmethod
    async def force_stop(cls, session: Session):
        t = session.t
        chat_id = session.chat_id
        if not SessionController.is_active_session(session.chat_id):
            await MessageController.send_nothing_to_stop(chat_id, t)
            return

        _session = SessionController.get_session(session.chat_id)  # get latest status
        if _session.status == SessionStatus.registration:
            await GameController.cancel_registration(chat_id, t)

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

        delta = time or 30  # todo replace "30" with settings registration extend/reduce time
        session.timer += delta * sign

        if sign >= 0:
            await MessageController.send_registration_extended(chat_id, t, delta, session.timer)
        else:
            await MessageController.send_registration_reduced(chat_id, t, delta, session.timer)
