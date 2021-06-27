from typing import TypedDict, List, Dict, Union
from aiogram.types import User


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'  # delete if unnecessary
    end = 'end'  # delete if unnecessary


class KilledPlayerData(TypedDict):
    user: User
    role: None  # todo replace with role type


KilledPlayersList = List[KilledPlayerData]

PlayersList = Dict[Union[str, int], User]

RolesList = Dict[Union[str, int], None]  # todo replace with role type