import asyncio
from typing import List, Tuple, Union, Callable, Awaitable, Dict
from bot.bot import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ContentType

from bot.types import ChatId, RoleMeta
from bot.utils.shared import async_wait


def arr2keyword_markup(buttons: List[List[Dict]]):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**btn) for btn in row] for row in buttons])


def parse_timer(text: str) -> Tuple[Union[int, None], int]:
    try:
        num = int(text.split(maxsplit=1)[1])
        return abs(num), -1 if num < 0 else 1
    except (ValueError, IndexError):
        return None, 1


async def attach_last_words(
        user_id: ChatId,
        text: str,
        callback: Callable[[Message], Awaitable[None]],
):
    await dp.bot.send_message(user_id, text)

    async def handler(msg, *args, **kwargs):
        dp.message_handlers.unregister(handler)
        await callback(msg)

    dp.register_message_handler(handler, chat_id=user_id, content_types=[ContentType.ANY])

    return handler


async def attach_mafia_chat(mafias: list[RoleMeta], spies: list[RoleMeta] = ()):
    mafia_dict = {maf.user.id: maf for maf in mafias}

    async def handler(msg: Message):
        user_id = msg.from_user.id
        if user_id not in mafia_dict or not mafia_dict[user_id].alive:
            return
        await asyncio.wait([msg.forward(subscriber.user.id) for subscriber in mafias if subscriber.alive])
        await async_wait([msg.copy_to(spy.user.id) for spy in spies if spy.alive])
        await msg.delete()

    dp.register_message_handler(handler, chat_id=[maf.user.id for maf in mafias], content_types=[ContentType.ANY])

    return handler
