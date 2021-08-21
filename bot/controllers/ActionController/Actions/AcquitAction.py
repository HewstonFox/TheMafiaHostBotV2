from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked


class AcquitAction(BaseAction):
    order = 5

    @is_blocked
    async def apply(self):
        self.target.acquit()
