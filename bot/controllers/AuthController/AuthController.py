import asyncio
from typing import Optional, Dict

import jwt
from aiogram.types import CallbackQuery
from jwt import InvalidTokenError

from bot.controllers import DispatcherProvider
from bot.controllers.MessageController.MessageController import MessageController
from bot.localization import Localization, get_default_translation
from bot.types import ChatId
from bot.utils.shared import is_error
from config import env


class AuthController(DispatcherProvider):
    __pending_auth = {}

    @classmethod
    async def auth(cls, user_id: ChatId, source: str, timeout: int = 20, t=get_default_translation()) -> Optional[str]:
        msg = await MessageController.send_authorization_request(user_id, t, source)
        if is_error(msg):
            return None

        key = f'{msg.message_id}:{user_id} {source}'
        cls.__pending_auth[key] = 0

        while timeout > 0 and cls.__pending_auth[key] == 0:
            timeout -= 1
            await asyncio.sleep(1)

        res = jwt.encode({"user_id": user_id}, env.JWT_KEY, algorithm="HS256") if cls.__pending_auth[key] == 1 else None
        cls.__pending_auth.pop(key, None)
        return res

    @classmethod
    def verify(cls, token: str) -> Optional[Dict]:
        if not token:
            return None
        try:
            return jwt.decode(token, env.JWT_KEY, algorithms="HS256")
        except InvalidTokenError:
            return None

    @classmethod
    async def callback_handler(cls, query: CallbackQuery, t: Localization):
        _, res, source = query.data.split()

        key = f'{query.message.message_id}:{query.from_user.id} {source}'

        if key not in cls.__pending_auth:
            await query.message.delete()
            return await query.answer(t.auth.failure)

        is_confirmed = res == '+'

        cls.__pending_auth[key] = 1 if is_confirmed else -1
        await query.message.edit_text(
            t.auth.request.format(source) +
            '\n\n' +
            (t.auth.options.confirm if is_confirmed else t.auth.options.reject)
        )

        return await query.answer(t.auth.success if is_confirmed else t.auth.reject)
