from bot.controllers.ActionController.Actions.BlockAction import BlockAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.Incognito import Incognito
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Whore(Incognito):
    shortcut = 'whr'

    async def affect(self, other: ChatId, key=None):
        self.action = BlockAction(self, self.players[other])
        await super(Whore, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
