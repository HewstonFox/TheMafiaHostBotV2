from typing import TypedDict, List, Dict, Union
from aiogram.types import User
from bson import ObjectId

from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'
    end = 'end'


class KilledPlayerData(TypedDict):
    user: User
    role: BaseRole


class SessionRecord(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    name: str
    status: str
    lang: str
    created_at: int
    updated_at: int


KilledPlayersList = List[KilledPlayerData]

PlayersList = Dict[Union[str, int], User]

RolesList = Dict[Union[str, int], BaseRole]
