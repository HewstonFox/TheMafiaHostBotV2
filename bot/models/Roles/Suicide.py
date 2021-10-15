from aiogram.types import User

from bot.controllers.SessionController.Session import Session
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team


class Suicide(Incognito):
    shortcut = 'scd'
    team = Team.scd

    def __init__(self, user: User, session: Session, index: int = 0):
        super().__init__(user, session, index)
        self.won = False

    def kill(self, by):
        super(Suicide, self).kill(by)
        if by == Team.civ:
            self.won = True

    async def send_action(self):
        return
