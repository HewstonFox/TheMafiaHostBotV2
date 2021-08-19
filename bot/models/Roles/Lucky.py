from random import choice

from bot.models.Roles.BaseRole import BaseRole


class Lucky(BaseRole):
    shortcut = 'lck'

    def kill(self, by: str):
        if choice((True, False)):
            super(BaseRole, self).kill(by)
            self.alive = False
