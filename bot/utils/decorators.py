from asyncio import sleep
from functools import wraps
from typing import Callable, Union
import traceback

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Unauthorized

from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus
from config import env
from database.session import get_session_record_by_chat_id, create_session_record
from localization import get_translation, Localization


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
            if issubclass(type(result), Exception):
                raise result
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


def with_locale(func: Callable[[Union[Message, CallbackQuery], Localization], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Union[Message, CallbackQuery]):
        return await func(msg, get_translation(msg.from_user.language_code))

    return wrapper


def with_session(func: Callable[[Union[Message, CallbackQuery], Session], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Union[Message, CallbackQuery]):
        chat = msg.chat
        session_record = await get_session_record_by_chat_id(chat.id)
        if not session_record:
            session_record = await create_session_record(
                chat_id=chat.id,
                name=chat.full_name,
                status=SessionStatus.pending,
                lang=msg.from_user.language_code or 'en'
            )
        session = Session.from_dict(session_record)
        return await func(msg, session)

    return wrapper


def clean_command(func: Callable[[Message, ...], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Message, *args, **kwargs):
        await msg.delete()
        return await func(msg, *args, **kwargs)

    return wrapper
