from asyncio import sleep
from functools import wraps
from typing import Callable
import traceback

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.exceptions import Unauthorized

from config import env


def message_retry(func: Callable) -> Callable:
    """func(self, *args, **kwargs)"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        i = 0
        while i < self.repeat:
            try:
                return await func(self, *args, **kwargs)
            except Unauthorized as e:
                return e
            except Exception as e:
                i += 1
                await sleep(1)
                if i == self.repeat:
                    return e

    return wrapper


def notify_error(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self: Bot, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            if issubclass(result, Exception):
                raise result
        except (Unauthorized, TypeError) as e:
            return e
        except Exception as e:
            print(e)
            await self.send_message(env.NOTIFICATION_CHAT, f"Error:\n`{traceback.format_exc()}`")
            return e

    return wrapper


def soft_error(func: Callable) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(e)
            return e

    return wrapper


def with_locale(func: Callable[[Message, str], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Message):
        return await func(msg, msg.from_user.language_code)

    return wrapper
