from bot.controllers.ActionController.Actions.VoteAction import DayKillVoteAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import players_list_menu_factory, get_description_factory, valid_player


class Incognito(BaseRole):
    team = Team.civ

    def vote(self, other: ChatId):
        self.action = DayKillVoteAction(self, self.players[other])

    async def send_vote(self):
        def select_target(key, _):
            check_result = valid_player(self.players, key)
            if all(check_result):
                self.vote(check_result[1].user.id)
                return True
            return False

        await MenuController.show_menu(
            self.user.id,
            players_list_menu_factory(
                'Vote for the player',
                list(self.players.values()),
            ),
            get_description_factory(self.players),
            select_target
        )
