from aiogram import Bot
from aiogram.types import CallbackQuery

from controllers.MessageSender import MessageSender
from localization import Localization


class CallbackQueryController:
    @classmethod
    async def more(cls, query, chat_id, bot, t):
        await MessageSender.send_private_more(bot, chat_id, t)
        await query.answer()

    @classmethod
    async def apply(cls, query: CallbackQuery, bot: Bot, t: Localization):
        return await getattr(cls, query.data.split()[0])(query, query.message.chat.id, bot, t)
