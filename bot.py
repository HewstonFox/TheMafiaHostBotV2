import logging
from typing import Callable

from aiogram import Dispatcher, executor, types, Bot
from aiogram.types import CallbackQuery

from bot_types import ChatType, CallbackQueryActions, ChatId
from bot_utils.decorators import with_locale
from config import env
from controllers.CallbackQueryController import CallbackQueryController
from controllers.MessageSender import MessageSender
from localization import Localization
from models.RetryBot import RetryBot

logging.basicConfig(level=logging.INFO if env.MODE == 'production' else logging.INFO)

bot = RetryBot(token=env.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot)


@dp.callback_query_handler()
@with_locale
async def callback_query_handler(query: CallbackQuery, t):
    await CallbackQueryController.apply(query, bot, t)


@dp.message_handler(commands=['start'])
@with_locale
async def start_handler(message: types.Message, t):
    args = (bot, message.chat.id, t)
    if message.chat.type == ChatType.private:
        await MessageSender.send_private_start_message(*args)
    else:
        pass


@dp.message_handler(commands=['game'])
async def start_handler(message: types.Message):
    await message.reply('U wrote game')


@dp.message_handler(commands=['stop'])
async def start_handler(message: types.Message):
    await message.reply('U wrote stop')


@dp.message_handler(commands=['extend'])
async def start_handler(message: types.Message):
    await message.reply('U wrote extend')


@dp.message_handler(commands=['reduce'])
async def start_handler(message: types.Message):
    await message.reply('U wrote reduce')


@dp.message_handler(commands=['leave'])
async def start_handler(message: types.Message):
    await message.reply('U wrote leave')


def start_bot():
    executor.start_polling(dp, skip_updates=True)
