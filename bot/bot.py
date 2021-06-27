import logging

from aiogram import Dispatcher
from config import env
from bot.models.RetryBot import RetryBot

logging.basicConfig(level=logging.INFO if env.MODE == 'production' else logging.INFO)

bot = RetryBot(token=env.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot)
