from aiogram.types import CallbackQuery

from bot.controllers.MessaggeController.MessageController import MessageController
from bot.types import ChatId
from localization import Localization


class CallbackQueryController:
    @classmethod
    async def more(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        await MessageController.send_private_more(chat_id, t)
        await query.answer()

    @classmethod
    async def add_player(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        print(chat_id)
        await query.answer()

    @classmethod
    async def apply(cls, query: CallbackQuery, t: Localization):
        return await getattr(cls, query.data.split()[0])(query, query.message.chat.id, t)
