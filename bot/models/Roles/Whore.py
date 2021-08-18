from bot.controllers.ActionController.Actions.BlockAction import BlockAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Whore(BaseRole):
    shortcut = 'whr'

    def affect(self, other: ChatId, key=None):
        self.action = BlockAction(self, self.players[other])

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
