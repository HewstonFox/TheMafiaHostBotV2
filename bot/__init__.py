import logging

from aiogram.utils import executor

from bot import handlers
from bot.bot import dp
from bot.commands import set_commands_list
from config import env


def start():
    logging.info(f'Starting in {env.MODE} mode.')
    if handlers:
        logging.info("Handlers attached")
    else:
        logging.error("Handlers NOT attached", handlers)
    executor.start_polling(dp, skip_updates=True, on_startup=set_commands_list)
