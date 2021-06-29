from typing import TypedDict

from bson import ObjectId

from bot.types import ChatId


class UserRecord(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    full_name: str
    username: str
    created_at: int
    updated_at: int
