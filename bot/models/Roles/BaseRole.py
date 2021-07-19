from typing import List

from aiogram.types import User

from bot.controllers.MessageController.MessageController import MessageController
from bot.localization import get_translation
from bot.models.Roles.RoleEffects import KillEffect, CureEffect, CheckEffect, BlockEffect, AcquitEffect


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

    def __init__(self, user: User):
        self.user = user
        self.shortcut = self.__class__.shortcut
        super(BaseRole, self).__init__()
        self.alive = True

    def kill(self, by: str):
        super(BaseRole, self).kill(by)
        self.alive = False

    async def greet(self):
        await MessageController.sent_role_greeting(get_translation(self.user.language_code), self.shortcut)

    async def affect(self, other: 'BaseRole'):
        return

    async def send_action(self, other: List['BaseRole']):
        return

    def __repr__(self):
        parents = [x.__name__ for x in self.__class__.__bases__ if type(x) != BaseRole]
        return f'<{self.__class__.shortcut or self.__class__.__name__}' \
               f'{" (" + ", ".join(parents) + ")" if len(parents) else ""}>'
