from typing import Callable, Any, Awaitable

from bot.models.Roles import BaseRole
from bot.utils.whore_tree import create_whore_tree


def is_blocked(func: Callable[['BaseAction'], Awaitable[Any]]):
    async def wrapper(self: 'BaseAction'):
        if not create_whore_tree(self, [player.action for player in self.actor.players.values() if
                                        player.action]).is_fucked():
            return await func(self)

    return wrapper


class BaseAction:
    order = -1
    is_blocker = False

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        self.actor = actor
        self.target = target

    @is_blocked
    async def apply(self):
        raise NotImplementedError

    def get_dump(self):
        return {
            'type': self.__class__.__name__,
            'order': self.order,
            'is_blocker': self.is_blocker,
            'actor': self.actor.user.id,
            'target': self.target.user.id,
        }
