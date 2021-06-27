from typing import Union, Dict

from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus
from bot.types import ChatId


class SessionController:
    __sessions: Dict[ChatId, Session] = {}

    @classmethod
    def create_session(cls, chat_id: ChatId) -> Union[Session, None]:
        if SessionController.is_active_session(chat_id):
            raise
        cls.__sessions[chat_id] = Session(chat_id)
        return cls.get_session(chat_id)

    @classmethod
    def get_session(cls, chat_id: ChatId) -> Union[Session, None]:
        return cls.__sessions[chat_id]

    @classmethod
    def kill_session(cls, chat_id: ChatId):
        session = cls.get_session(chat_id)
        if chat_id in cls.__sessions:
            del cls.__sessions[chat_id]
        session.status = SessionStatus.end
        return session

    @classmethod
    def is_active_session(cls, chat_id: ChatId):
        return chat_id in cls.__sessions
