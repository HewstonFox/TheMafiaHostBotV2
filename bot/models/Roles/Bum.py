from typing import List

from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.Spy import SpyAction
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


class Bum(BaseRole):
    shortcut = 'bum'

    def affect(self, other: ChatId):
        self.action = SpyAction(self, self.players[other])

    def answer(self, other: 'BaseRole', action: 'BaseAction'):
        if other.action:
            a = other
            b = other.action.target
        elif actors := [player.action.actor for player in self.players.values() if
                        player.action and player.action.target == other]:
            a = actors[0]
            b = other
        else:
            a = b = None

    def send_action(self, other: List['BaseRole']):
        raise NotImplementedError
