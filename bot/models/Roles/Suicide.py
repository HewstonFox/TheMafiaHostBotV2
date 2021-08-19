from aiogram.types import User

from bot.localization.Localization import Session
from bot.models.Roles.BaseRole import BaseRole


class Suicide(BaseRole):
    shortcut = 'scd'

    def __init__(self, user: User, session: Session):
        super().__init__(user, session)
        self.won = False
