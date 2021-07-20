from typing import List, Dict

from aiogram.types import User

from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


class Suicide(BaseRole):
    shortcut = 'scd'

    def __init__(self, user: User, players: Dict[ChatId, 'BaseRole'], settings: dict):
        super().__init__(user, players, settings)
        self.won = False

    def send_action(self, other: List['BaseRole']):
        raise NotImplementedError
