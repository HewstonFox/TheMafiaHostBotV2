from aiogram.types import User

from bot.controllers.ActionController.Actions.CureAction import CureAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.localization.Localization import Session
from bot.models.Roles.Incognito import Incognito
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Doctor(Incognito):
    shortcut = 'doc'

    def __init__(self, user: User, session: Session, index: int = 0):
        super().__init__(user, session, index)
        self._self_cure = 1

    async def affect(self, other: ChatId, key=None):
        if other == self.user.id:
            self._self_cure -= 1
        self.action = CureAction(self, self.players[other])
        await super(Doctor, self).affect(other, key)

    async def send_action(self):
        await MenuController.show_menu(
            **get_players_list_menu(self, lambda x: x.alive and (self._self_cure > 0 or x.user.id != self.user.id))
        )
