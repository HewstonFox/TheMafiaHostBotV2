from bot.controllers.ActionController.Actions.AcquitAction import AcquitAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Lawyer(Incognito):
    shortcut = 'lwr'
    team = Team.maf

    async def affect(self, other: ChatId, key=None):
        self.action = AcquitAction(self, self.players[other])
        await super(Lawyer, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
