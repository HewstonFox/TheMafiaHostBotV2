from typing import TypedDict, Union

from bson import ObjectId

from bot.types import ChatId
from bot.utils.shared import get_current_time
from database import db

users_collection = db.users


class UserRecord(TypedDict):
    _id: ObjectId
    chat_id: ChatId
    full_name: str
    username: str
    created_at: int
    updated_at: int


async def get_user_record_by_chat_id(chat_id: ChatId) -> Union[UserRecord, None]:
    return await users_collection.find_one({'chat_id': chat_id})


async def create_user_record(**kwargs) -> UserRecord:
    record: UserRecord = kwargs
    record['created_at'] = record['updated_at'] = get_current_time()
    await users_collection.insert_one(record)
    return await get_user_record_by_chat_id(record['chat_id'])


async def update_user_record(chat_id: ChatId, data: dict[str, any]) -> UserRecord:
    data['updated_at'] = get_current_time()
    await users_collection.update_one({'chat_id': chat_id}, {'$set': data})
    return await get_user_record_by_chat_id(chat_id)


async def check_if_user_record_exists(chat_id: ChatId) -> bool:
    return (await users_collection.count_documents({'chat_id': chat_id}, limit=1)) != 0
