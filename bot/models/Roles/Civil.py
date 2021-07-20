from typing import List

from bot.models.Roles.BaseRole import BaseRole


class Civil(BaseRole):

    shortcut = 'civ'

    def send_action(self, other: List['BaseRole']):
        raise NotImplementedError
