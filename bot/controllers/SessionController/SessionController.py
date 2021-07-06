from typing import Union, Dict

from aiogram import Dispatcher

from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.types import ChatId, Proxy


class SessionController:
    dp: Dispatcher

    __sessions: Proxy = Proxy({})

    @classmethod
    def create_session(cls, chat_id: ChatId) -> Union[Session, None]:
        if SessionController.is_active_session(chat_id):
            raise SessionAlreadyActiveError
        cls.__sessions[chat_id] = Session(chat_id)
        return cls.get_session(chat_id)

    @classmethod
    def push_session(cls, session: Session):
        s_id = session.chat_id
        if SessionController.is_active_session(s_id):
            raise SessionAlreadyActiveError
        cls.__sessions[s_id] = session

    @classmethod
    def get_session(cls, chat_id: ChatId) -> Union[Session, None]:
        return cls.__sessions[chat_id]

    @classmethod
    def kill_session(cls, chat_id: ChatId):
        session = cls.get_session(chat_id)
        if session:
            del cls.__sessions[chat_id]
        session.status = SessionStatus.end
        return session

    @classmethod
    def is_active_session(cls, chat_id: ChatId):
        return chat_id in cls.__sessions

    @classmethod
    async def leave_user(cls, session_id: ChatId, user_id: ChatId):
        session: Session = SessionController.get_session(session_id)
        if not session or not session.is_user_in(user_id):
            return

        session.remove_player(user_id)
        await MessageController.send_user_left_game(user_id, session)
