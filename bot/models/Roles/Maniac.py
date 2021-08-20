from bot.controllers.ActionController.Actions.KillAction import KillAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Maniac(BaseRole):
    shortcut = 'mnc'

    async def affect(self, other: ChatId, key=None):
        self.action = KillAction(self, self.players[other])
        await super(Maniac, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
