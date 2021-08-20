from bot.controllers.ActionController.Actions.VoteAction import MafiaKillVoteAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Mafia(BaseRole):
    shortcut = 'maf'

    async def affect(self, other: ChatId, key=None):
        if key != 'don':
            self.action = MafiaKillVoteAction(self, self.players[other])
        if all([pl.action for pl in self.players.values() if isinstance(pl, Mafia)]):
            await super(Mafia, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(
            self,
            lambda x: all((x.alive, self.user.id != x.user.id, not isinstance(x, Mafia)))
        ))
