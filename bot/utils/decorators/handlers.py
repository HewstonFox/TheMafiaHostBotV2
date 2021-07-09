from functools import wraps
from typing import Callable, Union

from aiogram.types import Message, CallbackQuery

from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.settings.Settings import Settings
from bot.controllers.SessionController.types import SessionStatus
from bot.localization import Localization, get_translation, get_default_translation_index


def with_locale(func: Callable[[Union[Message, CallbackQuery], Localization, ...], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Union[Message, CallbackQuery], *args, **kwargs):
        return await func(msg, get_translation(msg.from_user.language_code), *args, **kwargs)

    return wrapper


def with_session(func: Callable[[Union[Message, CallbackQuery], Session, ...], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Union[Message, CallbackQuery], *args, **kwargs):
        chat = msg.chat

        try:
            session = SessionController.get_session(chat.id)
        except KeyError:
            session = await Session.get_by_chat_id(chat.id)

        if not session:
            session = await Session.create(
                chat_id=chat.id,
                name=chat.full_name,
                status=SessionStatus.pending,
                settings=Settings(lang=msg.from_user.language_code or get_default_translation_index()).values
            )

        if chat.full_name != session.name:
            session.name = chat.full_name
            session.update()

        session.bot = msg.bot

        return await func(msg, session, *args, **kwargs)

    return wrapper


def clean_command(func: Callable[[Message, ...], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Message, *args, **kwargs):
        await msg.delete()
        return await func(msg, *args, **kwargs)

    return wrapper
