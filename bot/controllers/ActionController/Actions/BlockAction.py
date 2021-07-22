from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.models.Roles import BaseRole


class BlockAction(BaseAction):
    order = 1
    is_blocker = True

    @is_blocked
    async def apply(self):
        self.target.block()
