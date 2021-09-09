from aiogram.types import User

from bot.types import Proxy

Reactions = Proxy[str, list[User]]
