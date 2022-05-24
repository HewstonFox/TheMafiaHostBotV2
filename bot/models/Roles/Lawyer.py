from bot.controllers.ActionController.Actions.AcquitAction import AcquitAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MessageController.MessageController import MessageController
from bot.models.Roles.BaseRole import is_active_session
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu, get_roles_list


class Lawyer(Incognito):
    shortcut = 'lwr'
    team = Team.maf

    async def greet(self):
        await super(Lawyer, self).greet()
        team = [pl for pl in self.players.values() if pl.team == Team.maf]
        if len(team) > 0:
            await MessageController.send_team_greeting(self.user.id, self.t, self.shortcut, get_roles_list(team))

    @is_active_session
    async def affect(self, other: ChatId, key=None):
        self.action = AcquitAction(self, self.players[other])
        await super(Lawyer, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
