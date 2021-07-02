import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.controllers.CallbackQueryController.CallbackQueryController import CallbackQueryController
from bot.controllers.GameController.GameController import GameController
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.UserController.UserController import UserController
from config import env
from bot.models.RetryBot import RetryBot

logging.basicConfig(level=logging.INFO if env.MODE == 'production' else logging.INFO)

bot: Bot = RetryBot(token=env.BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def prepare_controllers():
    controllers = (
        CallbackQueryController,
        GameController,
        MessageController,
        SessionController,
        UserController
    )
    for controller in controllers:
        controller.dp = dp
