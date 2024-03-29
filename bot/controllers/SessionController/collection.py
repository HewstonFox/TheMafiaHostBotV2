from typing import Union

from bot.controllers.SessionController.types import SessionRecord
from bot.types import ChatId
from bot.utils.shared import get_current_time
from bot.db import db

sessions_collection = db.sessions


async def get_session_record_by_chat_id(chat_id: ChatId) -> Union[SessionRecord, None]:
    return await sessions_collection.find_one({'chat_id': chat_id})


async def create_session_record(**kwargs) -> SessionRecord:
    record: SessionRecord = kwargs
    record['created_at'] = record['updated_at'] = get_current_time()
    await sessions_collection.insert_one(record)
    return await get_session_record_by_chat_id(record['chat_id'])


async def update_session_record(chat_id: ChatId, data: dict[str, any]) -> SessionRecord:
    data['updated_at'] = get_current_time()
    await sessions_collection.update_one({'chat_id': chat_id}, {'$set': data})
    return await get_session_record_by_chat_id(chat_id)
