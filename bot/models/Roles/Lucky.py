from random import choice

from bot.models.Roles.BaseRole import BaseRole
from bot.models.Roles.Incognito import Incognito


class Lucky(Incognito):
    shortcut = 'lck'

    def kill(self, by: str):
        if choice((True, False)):
            super(BaseRole, self).kill(by)
            self.alive = False
