from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.models.Roles import BaseRole


class CheckAction(BaseAction):
    order = 10

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    def apply(self):
        self.actor.answer(self.target, self)
