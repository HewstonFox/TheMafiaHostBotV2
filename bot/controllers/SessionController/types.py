from typing import TypedDict, List, Dict, Union
from aiogram.types import User
from bson import ObjectId

from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId, Proxy


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'
    end = 'end'
    settings = 'settings'


class KilledPlayerData(TypedDict):
    user: User
    role: BaseRole


class SessionRecord(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    name: str
    status: str
    settings: dict
    created_at: int
    updated_at: int


KilledPlayersList = List[KilledPlayerData]

PlayersList = Proxy[Union[str, int], User]

RolesList = Proxy[Union[str, int], BaseRole]
