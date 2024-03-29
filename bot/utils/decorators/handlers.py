from functools import wraps
from typing import Callable, Union

from aiogram.types import Message, CallbackQuery, ChatMemberStatus

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

        session = SessionController.get_session(chat.id)
        if not session:
            session = await Session.get_by_chat_id(chat.id)
            if session and session.status != SessionStatus.pending:
                session.status = SessionStatus.pending

        if not session:
            session = await Session.create(
                chat_id=chat.id,
                name=chat.full_name,
                invite_url='',
                status=SessionStatus.pending,
                settings=Settings(lang=msg.from_user.language_code or get_default_translation_index()).values
            )

        should_update = False

        if chat.full_name != session.name:
            session.name = chat.full_name
            should_update = True

        if should_update:
            session.update()

        session.bot = msg.bot

        command = msg.get_command(pure=True)
        command_right = session.settings.values['command_rights'].get(command)
        user = msg.from_user
        if command_right and not ChatMemberStatus.is_chat_admin((await msg.chat.get_member(user.id)).status):
            await msg.bot.send_message(session.chat_id, f'You ({user.get_mention()}) have no rights'
                                                        f' for command <code>/{command}</code>')
            return

        return await func(msg, session, *args, **kwargs)

    return wrapper


def clean_command(func: Callable[[Message, ...], any]) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(msg: Message, *args, **kwargs):
        await msg.delete()
        return await func(msg, *args, **kwargs)

    return wrapper
