from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.Spy import SpyAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Bum(BaseRole):
    shortcut = 'bum'

    def affect(self, other: ChatId):
        self.action = SpyAction(self, self.players[other])

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        if other.action:
            a = other.user
            b = other.action.target.user
        elif actors := [player.action.actor for player in self.players.values()
                        if player.action and player.action.target == other]:
            a = actors[0].user
            b = other.user
        else:
            a = b = None

        if a and b:
            message = f"{a.get_mention()} visited {b.get_mention()}"  # todo add translation
        else:
            message = f"Nothing interesting happened with {other.user.get_mention()}"  # todo add translation
        await self.user.bot.send_message(self.user.id, message)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))