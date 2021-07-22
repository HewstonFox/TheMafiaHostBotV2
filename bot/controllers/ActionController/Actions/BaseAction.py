from bot.models.Roles import BaseRole


def is_blocked(func):
    def wrapper(self: 'BaseAction'):

        actor = self.actor
        blockers: list['BaseAction'] = [player.action for player in actor.players.values() if player.action.is_blocker]

        pipeline = [actor.user.id]

        while found := [
            blocker.actor.user.id for blocker in blockers
            if blocker.target.user.id == pipeline[-1]
        ]:
            if pipeline[0] in found:
                pipeline = []
                break
            pipeline.append(found)

        pipeline_len = len(pipeline)
        if pipeline_len and (pipeline_len == 1 or not (pipeline_len % 2)):
            unblock = self.actor.blocked  # setting property to false while reading it
            func(self)
        else:
            self.actor.block()

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
