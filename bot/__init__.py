import asyncio
import logging

from aiogram import Dispatcher
from aiogram.utils import executor

from bot import handlers
from bot.bot import dp
from bot.commands import set_commands_list
from bot.constants import WEBHOOK_URL, IS_WEBHOOK, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from bot.controllers.SessionController.SessionController import SessionController
from config import env


async def on_startup(dispatcher: Dispatcher):
    await set_commands_list(dispatcher)
    if IS_WEBHOOK:
        await dispatcher.bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher: Dispatcher):
    await SessionController.notify_shutdown(dispatcher)
    if IS_WEBHOOK:
        await dispatcher.bot.delete_webhook()


def start():
    logging.info(f'Starting in {env.MODE} mode.')
    logging.info(f'Connection type: {"webhook" if IS_WEBHOOK else "long-polling"}')
    if handlers:
        logging.info("Handlers attached")
    else:
        logging.error("Handlers NOT attached", handlers)

    options = {
        'dispatcher': dp,
        'on_startup': on_startup,
        'on_shutdown': on_shutdown,
        'skip_updates': True
    }

    if IS_WEBHOOK:
        executor.start_webhook(
            **options,
            loop=asyncio.get_event_loop(),
            webhook_path=WEBHOOK_PATH,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(
            **options,
        )
