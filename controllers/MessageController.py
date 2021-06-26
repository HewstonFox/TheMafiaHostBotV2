from aiogram import Bot

from bot_types import ChatId
from localization import t


class MessageController:
    @classmethod
    async def send_private_start_message(cls, bot: Bot, chat_id: ChatId, locale):
        await bot.send_message(chat_id, t(locale).language)
