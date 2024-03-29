import asyncio
from typing import Callable

from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled

from bot.bot import dp


def throttle_message_handler(*args, **kwargs):
    def wrapper(func: Callable):
        @dp.message_handler(*args, **kwargs)
        async def _wrapper(msg: Message, *_args, **_kwargs):
            try:
                if 'commands' in kwargs:
                    throttle_key = ''.join(kwargs['commands'])
                else:
                    throttle_key = msg.text
                await dp.throttle(throttle_key, rate=3, chat_id=msg.chat.id)
            except Throttled:
                pass
            else:
                asyncio.create_task(func(msg, *_args, **_kwargs))

        return _wrapper

    return wrapper


def throttle_callback_query_handler():
    def wrapper(func: Callable):
        @dp.callback_query_handler()
        async def _wrapper(query: CallbackQuery, *args, **kwargs):
            try:
                data = query.data.split()
                await dp.throttle(data[0] if data else '~', rate=.3, chat_id=query.message.chat.id, user_id=query.from_user.id)
            except Throttled:
                return
            else:
                return await func(query, *args, **kwargs)

        return _wrapper

    return wrapper
