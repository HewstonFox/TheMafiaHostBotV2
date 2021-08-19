from bot.controllers.ActionController.Actions.VoteAction import DonKillVoteAction
from bot.models.Roles.Mafia import Mafia
from bot.types import ChatId


class Don(Mafia):
    shortcut = 'don'

    def affect(self, other: ChatId):
        self.action = DonKillVoteAction(self, self.players[other])
