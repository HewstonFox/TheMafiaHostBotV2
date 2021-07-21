from typing import List, Optional, Dict

from aiogram.types import User

from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.Spy import SpyAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.roles import valid_player


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
        def get_description(key):
            check_result = valid_player(self.players, key)
            if all(check_result):
                return f'You choose {check_result[1].user.get_mention()}'
            return 'This player is not in game'

        def select_target(key, _):
            check_result = valid_player(self.players, key)
            if all(check_result):
                self.affect(check_result[1].user.id)
                return True
            return False

        await MenuController.show_menu(self.user.id, MessageMenu(
            description='Select target to spy',
            disable_special_buttons=True,
            buttons=[MessageMenuButton(
                type=ButtonType.endpoint,
                name=pl.user.full_name,
                key=str(pl.user.id)
            ) for pl in self.players.values() if pl.user.id != self.user.id]
        ), get_description, select_target)
