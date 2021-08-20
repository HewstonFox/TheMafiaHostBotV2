from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.models.Roles.constants import Team


class KillAction(BaseAction):
    order = 15

    @is_blocked
    async def apply(self):
        self.target.kill(self.actor.shortcut)


class IncognitoKillAction(KillAction):
    async def apply(self):
        self.target.kill(Team.civ)
