from typing import Union, Dict

from bot_types import ChatId
from models.Session import Session


class SessionManager:
    __sessions: Dict[ChatId, Session] = []

    @classmethod
    def create_session(cls, chat_id: ChatId) -> Union[Session, None]:
        cls.__sessions[chat_id] = Session(chat_id)
        return cls.get_session(chat_id)

    @classmethod
    def get_session(cls, chat_id: ChatId) -> Union[Session, None]:
        return cls.__sessions[chat_id]

    @classmethod
    def kill_session(cls, chat_id: ChatId):
        session = cls.get_session(chat_id)
        if chat_id in cls.__sessions.keys():
            del cls.__sessions[chat_id]
        # stop session instance
        return session
