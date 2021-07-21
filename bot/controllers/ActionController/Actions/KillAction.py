from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.models.Roles import BaseRole


class KillAction(BaseAction):
    order = 15

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    async def apply(self):
        self.target.kill(self.actor.shortcut)
