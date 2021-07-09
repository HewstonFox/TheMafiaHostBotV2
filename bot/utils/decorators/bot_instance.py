import traceback
from asyncio import sleep
from functools import wraps
from typing import Callable

from aiogram import Bot
from aiogram.utils.exceptions import Unauthorized, MessageToDeleteNotFound, MessageToReplyNotFound, RetryAfter, \
    MessageNotModified, InvalidQueryID

from bot.utils.shared import raise_if_error
from config import env


def message_retry(func: Callable) -> Callable:
    """func(self, *args, **kwargs)"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        i = 0
        while i < self.repeat:
            try:
                return await func(self, *args, **kwargs)
            except (
                    Unauthorized,
                    MessageToDeleteNotFound,
                    MessageToReplyNotFound,
                    MessageNotModified,
                    InvalidQueryID
            ) as e:
                return e
            except RetryAfter as e:
                await sleep(e.timeout)
            except Exception as e:
                print(e)
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
            raise_if_error(result)
            return result
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
