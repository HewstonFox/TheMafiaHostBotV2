from typing import List, Optional, Dict

from aiogram.types import User

from bot.controllers.MessageController.MessageController import MessageController
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
    shortcut: str = ''

    def __init__(self, user: User, players: Dict[ChatId, 'BaseRole'], settings: dict):
        self.action: Optional['BaseAction'] = None
        self.user = user
        self.shortcut = self.__class__.shortcut
        super(BaseRole, self).__init__()
        self.alive = True
        self.settings = settings
        self.players = players

    def kill(self, by: str):
        super(BaseRole, self).kill(by)
        self.alive = False

    async def greet(self):
        await MessageController.sent_role_greeting(get_translation(self.user.language_code), self.shortcut)

    async def affect(self, other: ChatId):
        return

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        return

    async def send_action(self, other: List['BaseRole']):
        return

    def __repr__(self):
        parents = [x.__name__ for x in self.__class__.__bases__ if type(x) != BaseRole]
        return f'<{self.__class__.shortcut or self.__class__.__name__}' \
               f'{" (" + ", ".join(parents) + ")" if len(parents) else ""}>'
