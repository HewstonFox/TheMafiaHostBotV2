import logging
from aiogram import Dispatcher, executor, types

from config import env
from models.RetryBot import RetryBot

logging.basicConfig(level=logging.INFO if env.MODE == 'production' else logging.DEBUG)

bot = RetryBot(token=env.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot)


@dp.callback_query_handler()
async def callback_query_handler(query: types.CallbackQuery):
    print(query)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('U wrote start')


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
