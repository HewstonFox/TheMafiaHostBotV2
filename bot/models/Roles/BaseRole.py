from typing import List, Optional, Dict

from aiogram.types import User

from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.localization import get_translation
from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.models.Roles.RoleEffects import KillEffect, CureEffect, CheckEffect, BlockEffect, AcquitEffect
from bot.types import ChatId


class Meta(type):
    def __repr__(cls):
        parents = [x.__name__ for x in cls.__bases__ if x != BaseRole]
        return f'<{cls.__name__}{" (" + ", ".join(parents) + ")" if len(parents) else ""}>'


class BaseRole(
    KillEffect,
    CureEffect,
    CheckEffect,
    BlockEffect,
    AcquitEffect,
    metaclass=Meta,
):
    shortcut: str = 'base'

    def __init__(self, user: User, session: Session):
        self.action: Optional['BaseAction'] = None
        self.user = user
        super(BaseRole, self).__init__()
        self.alive = True
        self.settings = session.settings.values
        self.players = session.roles
        self.t = session.t

    def kill(self, by: str):
        super(BaseRole, self).kill(by)
        self.alive = False

    async def greet(self):
        await MessageController.sent_role_greeting(self.user.id, self.t, self.shortcut)

    async def affect(self, other: ChatId):
        return

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        return

    async def send_action(self):
        return

    def __repr__(self):
        parents = [x.__name__ for x in self.__class__.__bases__ if type(x) != BaseRole]
        return f'<{self.__class__.shortcut or self.__class__.__name__}' \
               f'{" (" + ", ".join(parents) + ")" if len(parents) else ""}>'
