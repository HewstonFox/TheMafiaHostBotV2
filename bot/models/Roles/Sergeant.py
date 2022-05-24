from bot.controllers.MessageController.MessageController import MessageController
from bot.models.Roles.Incognito import Incognito
from bot.utils.roles import get_roles_list


class Sergeant(Incognito):
    shortcut = 'srg'

    async def greet(self):
        await super(Sergeant, self).greet()
        team = [pl for pl in self.players.values() if isinstance(pl, Sergeant)]
        if len(team) > 0:
            await MessageController.send_team_greeting(self.user.id, self.t, self.shortcut, get_roles_list(team))

    async def send_action(self):
        return
