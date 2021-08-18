from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.models.Roles import BaseRole


class CheckAction(BaseAction):
    order = 10

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    @is_blocked
    async def apply(self):
        self.target.check()
        await self.actor.answer(self.target, self)
