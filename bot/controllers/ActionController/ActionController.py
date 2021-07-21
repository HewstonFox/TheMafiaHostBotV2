from typing import Dict

from bot.controllers import BaseController
from bot.models.Roles import BaseRole
from bot.types import ChatId


class ActionController(BaseController):

    @classmethod
    async def apply_actions(cls, players: Dict[ChatId, BaseRole]):
        actions = sorted([player.action for player in players.values()], key=lambda x: x.order)

        for action in actions:
            await action.apply()
