from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.bot import bot
from bot.types import MarkupKeyboardDict, ChatId


def arr2keyword_markup(buttons: List[List[MarkupKeyboardDict]]):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**btn) for btn in row] for row in buttons])


async def cleanup_messages(chat_id: ChatId, ids: List[ChatId]):
    for msg_id in ids:
        await bot.delete_message(chat_id, msg_id)
