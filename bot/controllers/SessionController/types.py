from typing import TypedDict, List, Union
from aiogram.types import User
from bson import ObjectId

from bot.types import ChatId, Proxy


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'


class SessionRecord(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    name: str
    status: str
    settings: dict
    created_at: int
    updated_at: int


PlayersList = Proxy[Union[str, int], User]

RolesList = Proxy[Union[str, int], 'bot.models.Roles.BaseRole.BaseRole']
