from functools import wraps
from typing import Callable

from aiogram.types import Message
from aiogram.utils.exceptions import Throttled

from bot.bot import dp


def throttle_message_handler(*args, **kwargs):
    def wrapper(func: Callable):
        @dp.message_handler(*args, **kwargs)
        async def _wrapper(msg: Message, *_args, **_kwargs):
            try:
                await dp.throttle(''.join(kwargs['commands']), rate=3, chat_id=msg.chat.id)
            except Throttled:
                return
            else:
                return await func(msg, *_args, **_kwargs)

        return _wrapper

    return wrapper
