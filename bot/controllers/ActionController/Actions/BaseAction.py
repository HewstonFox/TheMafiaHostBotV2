from bot.models.Roles import BaseRole


def is_blocked(func):
    def wrapper(self):
        if not self.actor.blocked:
            func()

    return wrapper


class BaseAction:
    order = -1

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        self.actor = actor
        self.target = target
        self.order = self.__class__.order

    @is_blocked
    async def apply(self):
        raise NotImplementedError
