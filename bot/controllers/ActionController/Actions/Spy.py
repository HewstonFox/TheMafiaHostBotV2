from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked


class SpyAction(BaseAction):
    order = 5

    @is_blocked
    async def apply(self):
        await self.actor.answer(self.target, self)
