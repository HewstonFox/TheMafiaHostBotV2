from typing import List, Tuple, Union, Callable, Awaitable

from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ContentType

from bot.types import MarkupKeyboardDict, ChatId


def arr2keyword_markup(buttons: List[List[MarkupKeyboardDict]]):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**btn) for btn in row] for row in buttons])


def parse_timer(text: str) -> Tuple[Union[int, None], int]:
    try:
        num = int(text.split(maxsplit=1)[1])
        return abs(num), -1 if num < 0 else 1
    except (ValueError, IndexError):
        return None, 1


async def attach_last_words(
        dp: Dispatcher,
        user_id: ChatId,
        text: str,
        callback: Callable[[Message], Awaitable[None]],
):
    await dp.bot.send_message(user_id, text)

    async def handler(msg, *args, **kwargs):
        dp.message_handlers.unregister(handler)
        await callback(msg)

    dp.register_message_handler(handler, chat_id=user_id, content_types=[
        ContentType.ANY
    ])

    return handler
