from typing import TypedDict, List, Dict, Union
from aiogram.types import User

from bot.models.Roles.BaseRole import BaseRole


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'
    end = 'end'


class KilledPlayerData(TypedDict):
    user: User
    role: BaseRole


KilledPlayersList = List[KilledPlayerData]

PlayersList = Dict[Union[str, int], User]

RolesList = Dict[Union[str, int], BaseRole]
