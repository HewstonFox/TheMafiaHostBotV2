from typing import TypedDict

from bson import ObjectId

from bot.types import ChatId


class _UserRecordBase(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    full_name: str
    username: str
    created_at: int
    updated_at: int


class UserRecord(_UserRecordBase, total=False):
    is_admin: bool
