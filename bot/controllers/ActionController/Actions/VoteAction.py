from typing import Optional

from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.models.Roles import BaseRole


class VoteAction(BaseAction):
    order = 5

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    @is_blocked
    async def apply(self) -> Optional[bool]:
        return True
