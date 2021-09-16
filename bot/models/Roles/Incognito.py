from bot.controllers.ActionController.Actions.VoteAction import DayKillVoteAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.SessionController.settings.constants import DisplayType
from bot.models.Roles.BaseRole import BaseRole
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import players_list_menu_factory, get_description_factory, select_target_factory


class Incognito(BaseRole):
    team = Team.civ

    async def vote(self, other: ChatId, *args, **kwargs):
        target: BaseRole = self.players[other]
        self.action = DayKillVoteAction(self, target)
        display_type = self.settings['game']['show_message_on_vote']
        if display_type == DisplayType.show:
            text = f'{self.user.get_mention()} voted for {target.user.get_mention()}.'
        elif display_type == DisplayType.partially:
            text = f'{self.user.get_mention()} voted.'
        else:
            return
        await self.session.bot.send_message(self.session.chat_id, text)

    async def send_vote(self):
        await MenuController.show_menu(
            self.user.id,
            players_list_menu_factory(
                'Vote for the player',
                list(self.players.values()),
            ),
            get_description_factory(self.players, self, False),
            select_target_factory(self.players, self, False, 'vote'),
            self.t
        )
