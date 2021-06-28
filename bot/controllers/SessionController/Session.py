import asyncio

from aiogram.types import User

from bot.controllers.SessionController.types import PlayersList, RolesList, KilledPlayersList, SessionStatus
from bot.models import MafiaBotError
from bot.models.MafiaBotError import InvalidSessionStatusError
from bot.types import ChatId
from database.session import SessionRecord, change_session_record_status
from localization import Localization, get_translation


class Session:
    def __init__(self,
                 chat_id: ChatId,
                 name: str = '',
                 status: str = SessionStatus.pending,
                 lang: str = 'en',
                 **kwargs
                 ):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionIdError
        self.chat_id: ChatId = chat_id
        self.name = name
        self.players: PlayersList = {}
        self.roles: RolesList = {}
        self.killed: KilledPlayersList = []
        self.t: Localization = get_translation(lang)
        self.__status: str = status

    def add_player(self, user: User):
        self.players[user.id] = user
        print(self.players)

    def is_user_in(self, user_id: ChatId):
        return user_id in self.players

    def remove_player(self, user_id):
        self.players.pop(user_id)

    def __del__(self):
        self.status = SessionStatus.pending

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in SessionStatus.__dict__.values():
            raise InvalidSessionStatusError
        asyncio.create_task(change_session_record_status(self.chat_id, value))
        self.__status = value

    @classmethod
    def from_dict(cls, obj: SessionRecord):
        return Session(**obj)
