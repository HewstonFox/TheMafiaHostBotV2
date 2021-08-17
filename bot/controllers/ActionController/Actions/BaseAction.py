from bot.models.Roles import BaseRole
from bot.utils.whore_tree import create_whore_tree


def is_blocked(func):
    def wrapper(self: 'BaseAction'):
        if not create_whore_tree(self, [player.action for player in self.actor.players.values()]).is_fucked():
            func(self)

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
