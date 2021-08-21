from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked


class CheckAction(BaseAction):
    order = 10

    @is_blocked
    async def apply(self):
        self.target.check()
        await self.actor.answer(self.target, self)
