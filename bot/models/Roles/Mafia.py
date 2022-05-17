from bot.controllers.ActionController.Actions.VoteAction import MafiaKillVoteAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MessageController.MessageController import MessageController
from bot.models.Roles.BaseRole import is_active_session
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Mafia(Incognito):
    shortcut = 'maf'
    team = Team.maf
    is_angry = True

    @is_active_session
    async def affect(self, other: ChatId, key=None):
        if key != 'don':
            self.action = MafiaKillVoteAction(self, self.players[other])
        victim: Incognito = list(filter(lambda x: x.user.id == other, self.players.values()))[0]
        mafias = [pl for pl in self.players.values() if isinstance(pl, Mafia) and pl.alive]
        for maf in mafias:
            if maf == self:
                continue
            await MessageController.send_actor_chose_victim(
                maf.user.id, maf.t,
                self.user.get_mention(), victim.user.get_mention()
            )
        if all([pl.action for pl in mafias]):
            await super(Mafia, self).affect(other)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(
            self,
            lambda x: all((x.alive, self.user.id != x.user.id, not isinstance(x, Mafia)))
        ))
