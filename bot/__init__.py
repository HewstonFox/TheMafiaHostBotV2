import logging

from aiogram.utils import executor

from bot import handlers
from bot.bot import dp, prepare_controllers
from config import env


def start():
    logging.info(f'Starting in {env.MODE} mode.')
    if handlers:
        logging.info("Handlers attached")
    else:
        logging.error("Handlers NOT attached", handlers)
    prepare_controllers()
    executor.start_polling(dp, skip_updates=True)
