from aiogram.types import User

from bot.controllers.SessionController.types import PlayersList, RolesList, KilledPlayersList, SessionStatus
from bot.models import MafiaBotError
from bot.types import ChatId


class Session:
    def __init__(self, chat_id: ChatId):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionId
        self.chat_id: ChatId = chat_id
        self.players: PlayersList = {}
        self.roles: RolesList = {}
        self.killed: KilledPlayersList = []
        self.__status: str = SessionStatus.registration

    def add_player(self, user: User):
        self.players[user.id] = user

    def remove_player(self, user_id):
        self.players.pop(user_id)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in SessionStatus.__dict__.values():
            raise
        self.__status = value
