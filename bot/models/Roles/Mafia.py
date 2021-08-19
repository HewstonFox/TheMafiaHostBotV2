from bot.controllers.ActionController.Actions.VoteAction import MafiaKillVoteAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Mafia(BaseRole):
    shortcut = 'maf'

    def affect(self, other: ChatId):
        self.action = MafiaKillVoteAction(self, self.players[other])

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(
            self,
            lambda x: all((x.alive, self.user.id != x.user.id, not isinstance(x, Mafia)))
        ))
