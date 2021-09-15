from typing import Optional, Callable, Any, Awaitable

from aiogram.types import User

from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus
from bot.models.Roles.RoleEffects import KillEffect, CureEffect, CheckEffect, BlockEffect, AcquitEffect
from bot.types import ChatId, RoleMeta


class Meta(type):
    def __repr__(cls):
        parents = [x.__name__ for x in cls.__bases__ if x != BaseRole]
        return f'<{cls.__name__}{" (" + ", ".join(parents) + ")" if len(parents) else ""}>'


def is_active_session(fn: Callable[['BaseRole', Any], Awaitable[Any]]):
    async def wrapper(self: 'BaseRole', *args, **kwargs):
        if self.session.status != SessionStatus.game:
            return
        await fn(self, *args, **kwargs)

    return wrapper


class BaseRole(
    RoleMeta,
    KillEffect,
    CureEffect,
    CheckEffect,
    BlockEffect,
    AcquitEffect,
    metaclass=Meta,
):
    shortcut: str = 'base'
    team: str = ''

    def __init__(self, user: User, session: Session, index: int = 0):
        self.action: Optional['BaseAction'] = None
        self.user = user
        super(BaseRole, self).__init__()
        self.won = True
        self.alive = True
        self.session = session
        self.settings = session.settings.values
        self.players = session.roles
        self.t = session.t
        self.index = index

    def kill(self, by: str):
        if self.CURED:
            return
        super(BaseRole, self).kill(by)
        self.alive = False
        self.won = False

    async def greet(self):
        await MessageController.send_role_greeting(self.user.id, self.t, self.shortcut)

    async def affect(self, other: ChatId, key: Optional[str] = None):
        if self.session.settings.values['game']['show_night_actions']:
            await self.session.bot.send_message(self.session.chat_id, f'{self.shortcut} moved')  # todo: add translation

    async def send_promotion(self):
        # maybe better to do just initial greet in place of this
        await self.session.bot.send_message(self.user.id, f'You are {self.shortcut} from now')  # todo: add translation

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        return

    async def send_action(self):
        return

    async def vote(self, other: ChatId, *args, **kwargs):
        raise NotImplementedError

    async def send_vote(self):
        raise NotImplementedError

    def __repr__(self):
        parents = [x.__name__ for x in self.__class__.__bases__ if type(x) != BaseRole]
        return f'<{self.__class__.shortcut or self.__class__.__name__}' \
               f'{" (" + ", ".join(parents) + ")" if len(parents) else ""} {self.user.full_name}>'

    def get_dump(self):
        return {k: v.id if k == 'user' else v for k, v in self.__dict__.items() if
                k not in ('t', 'session', 'settings', 'players')}
