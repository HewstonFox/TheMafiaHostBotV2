from random import shuffle

from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.Spy import SpyAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.models.Roles.BaseRole import BaseRole, is_active_session
from bot.models.Roles.Incognito import Incognito
from bot.types import ChatId
from bot.utils.roles import get_players_list_menu


class Bum(Incognito):
    shortcut = 'bum'

    @is_active_session
    async def affect(self, other: ChatId, key=None):
        self.action = SpyAction(self, self.players[other])
        await super(Bum, self).affect(other, key)

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        if other.action:
            a = other.user
            b = other.action.target.user
        elif actors := [player.action.actor for player in self.players.values()
                        if player.action and player.action.target == other and player.user != self.user]:
            shuffle(actors)
            a = actors[0].user
            b = other.user
        else:
            a = b = None

        if a and b:
            message = self.t.roles.chore.bum.actor_visited_target.format(a.get_mention(), b.get_mention())
        else:
            message = self.t.roles.chore.bum.nothing_interesting.format(other.user.get_mention())
        await self.user.bot.send_message(self.user.id, message)

    async def send_action(self):
        await MenuController.show_menu(**get_players_list_menu(self, lambda x: x.alive and self.user.id != x.user.id))
