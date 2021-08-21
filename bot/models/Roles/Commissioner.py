import asyncio

from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.CheckAction import CheckAction
from bot.controllers.ActionController.Actions.KillAction import KillAction
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType
from bot.models.Roles import BaseRole
from bot.models.Roles.Sergeant import Sergeant
from bot.models.Roles.constants import Team
from bot.types import ChatId
from bot.utils.roles import get_description_factory, select_target_factory


class Commissioner(Sergeant):
    shortcut = 'com'

    class __Actions:
        check = 'check'
        kill = 'kill'

    async def affect(self, other: ChatId, key=None):
        action = self.__Actions.kill if key.startswith(self.__Actions.kill) else self.__Actions.check
        self.action = (KillAction if action == self.__Actions.kill else CheckAction)(self, self.players[other])
        await self.user.bot.send_message(self.session.chat_id,
                                         f'{self.shortcut} moved as {action}')  # todo: add translation

    async def answer(self, other: 'BaseRole', action: 'BaseAction'):
        role = Team.civ if other.ACQUITTED else other.shortcut
        for sheriff in [shr for shr in self.players.values() if isinstance(shr, Sergeant)]:
            asyncio.create_task(self.user.bot.send_message(
                sheriff.user.id,
                f'*{other.user.get_mention()} is {role}'  # todo: add translation
            ))

    async def send_action(self):
        #  todo add translation for whole menu
        players = [pl for pl in self.players.values() if pl.alive and pl.user.id != self.user.id]
        await MenuController.show_menu(
            self.user.id,
            MessageMenu(
                description='*Choose an action',
                disable_special_buttons=True,
                buttons=[
                            MessageMenuButton(
                                type=ButtonType.route,
                                name='*Kill',
                                description='*Choose a target',
                                buttons=[MessageMenuButton(
                                    type=ButtonType.endpoint,
                                    name=pl.user.full_name,
                                    key=f'{self.__Actions.kill}:{pl.user.id}'
                                ) for pl in players]
                            ),
                            MessageMenuButton(
                                type=ButtonType.route,
                                name='*Check',
                                description='*Choose a target',
                                buttons=[MessageMenuButton(
                                    type=ButtonType.endpoint,
                                    name=pl.user.full_name,
                                    key=f'{self.__Actions.check}:{pl.user.id}'
                                ) for pl in players]
                            ),
                        ][0 if self.settings['game']['commissioner_can_kill'] else 1:]
            ),
            get_description_factory(self.players),
            select_target_factory(self.players, self)
        )
