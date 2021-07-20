from typing import Dict, List

from aiogram.types import User

from bot.controllers.ActionController.Actions.CureAction import CureAction
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


class Doctor(BaseRole):
    shortcut = 'doc'

    def __init__(self, user: User, players: Dict[ChatId, 'BaseRole'], settings: dict):
        super().__init__(user, players, settings)
        self._self_cure = 1

    def affect(self, other: ChatId):
        if other == self.user.id:
            self._self_cure -= 1
        self.action = CureAction(self, self.players[other])

    def send_action(self, other: List['BaseRole']):
        raise NotImplementedError
