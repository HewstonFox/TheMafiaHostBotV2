from asyncio import sleep

from bot.controllers.MessaggeController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.types import ChatId
from bot.utils.message import cleanup_messages
from localization import Localization


class GameController:

    @classmethod
    async def run_new_game(cls, chat_id: ChatId, session: Session, time: int = None):
        t = session.t
        try:
            SessionController.push_session(session)
        except SessionAlreadyActiveError:
            await MessageController.send_registration_is_already_started(chat_id, t)
            return
        msg = await MessageController.send_registration_start(chat_id, t)
        timer = time or 60 * 1
        to_clean_msg = [msg.message_id]
        session.status = SessionStatus.registration
        while timer:
            if session.status != SessionStatus.registration:
                break
            await sleep(1)
            timer -= 1
            if not timer % 10:
                m = await MessageController.send_registration_reminder(chat_id, t, timer, to_clean_msg[0])
                to_clean_msg.append(m.message_id)
        await cleanup_messages(chat_id, to_clean_msg)
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
    async def force_stop(cls, chat_id: ChatId, session: Session):
        t = session.t
        if not SessionController.is_active_session(session.chat_id):
            await MessageController.send_nothing_to_stop(chat_id, t)
            return

        if session.status == SessionStatus.registration:
            await GameController.cancel_registration(chat_id, t)
