from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_types import ChatId, CallbackQueryActions
from localization import Localization


class MessageSender:
    @classmethod
    async def send_private_start_message(cls, bot: Bot, chat_id: ChatId, t: Localization):
        inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(t.private.button.more, callback_data=CallbackQueryActions.more)]])
        await bot.send_message(chat_id, t.private.start, reply_markup=inline_keyboard)

    @classmethod
    async def send_private_more(cls, bot, chat_id, t):
        await bot.send_message(chat_id, "Bot`s more, add transition")
