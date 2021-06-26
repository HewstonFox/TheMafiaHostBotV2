from aiogram.types import User

from bot_types import KilledPlayersList, PlayersList, RolesList, SessionStatus, ChatId
from models import MafiaBotError


class Session:
    def __init__(self, chat_id: ChatId):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionId
        self.chat_id: ChatId = chat_id
        self.players: PlayersList = {}
        self.roles: RolesList = {}
        self.killed: KilledPlayersList = []
        self.status: str = SessionStatus.registration

    def add_player(self, user: User):
        self.players[user.id] = user

    def remove_player(self, user_id):
        self.players.pop(user_id)
