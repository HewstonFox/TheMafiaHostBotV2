from bot.controllers.ActionController.Actions.VoteAction import DonKillVoteAction
from bot.models.Roles.Mafia import Mafia
from bot.types import ChatId


class Don(Mafia):
    shortcut = 'don'

    async def affect(self, other: ChatId, key=None):
        self.action = DonKillVoteAction(self, self.players[other])
        await super(Don, self).affect(other, self.shortcut)
