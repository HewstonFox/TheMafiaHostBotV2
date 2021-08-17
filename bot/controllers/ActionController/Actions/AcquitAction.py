from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.models.Roles import BaseRole


class AcquitAction(BaseAction):
    order = 5

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    async def apply(self):
        self.target.acquit()