import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.controllers import DispatcherProvider
from config import env
from bot.models.RetryBot import RetryBot

logging.basicConfig(level=logging.INFO if env.MODE == 'production' else logging.DEBUG)

bot: Bot = RetryBot(token=env.BOT_TOKEN, parse_mode='html')

dp = Dispatcher(bot, storage=MemoryStorage(), loop=asyncio.get_event_loop())

dp.middleware.setup(LoggingMiddleware())

DispatcherProvider.dp = dp
