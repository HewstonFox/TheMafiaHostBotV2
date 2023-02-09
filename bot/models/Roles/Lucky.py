from random import choice

from bot.models.Roles.Incognito import Incognito


class Lucky(Incognito):
    shortcut = 'lck'

    def kill(self, by: str):
        if choice((True, False)):
            super(Lucky, self).kill(by)
