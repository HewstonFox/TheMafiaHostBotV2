import signal
import sys
import asyncio
import logging
from typing import Optional

from aiogram import Dispatcher
from aiogram.dispatcher.webhook import DEFAULT_ROUTE_NAME
from aiogram.utils.executor import start_polling, set_webhook
from aiohttp.web_app import Application

import bot.routes
from bot import handlers
from bot.bot import dp
from bot.commands import set_commands_list
from bot.constants import WEBHOOK_URL, IS_WEBHOOK, WEBHOOK_PATH, WEBAPP_HOST, \
    WEBAPP_PORT, IS_PING_PONG
from bot.controllers.GameController.GameController import GameController
from bot.utils.shared import ping_pong
from config import env


# Default start_webhook function not allows to set web_app
def start_webhook(
        dispatcher, webhook_path, *,
        loop=None, skip_updates=None,
        on_startup=None, on_shutdown=None,
        check_ip=False, retry_after=None,
        route_name=DEFAULT_ROUTE_NAME, web_app: Optional[Application] = None,
        **kwargs
):
    executor = set_webhook(
        dispatcher=dispatcher, webhook_path=webhook_path,
        loop=loop, skip_updates=skip_updates,
        on_startup=on_startup, on_shutdown=on_shutdown,
        check_ip=check_ip, retry_after=retry_after,
        route_name=route_name,
        web_app=web_app
    )
    executor.run_app(**kwargs)


async def on_startup_callback(dispatcher: Dispatcher):
    def sys_exit(*_):
        sys.exit(2)

    signal.signal(signal.SIGINT, sys_exit)
    signal.signal(signal.SIGTERM, sys_exit)
    await set_commands_list(dispatcher)
    if IS_WEBHOOK:
        await dispatcher.bot.set_webhook(WEBHOOK_URL)
        if IS_PING_PONG:
            asyncio.create_task(ping_pong())


async def on_shutdown_callback(dispatcher: Dispatcher):
    await GameController.shutdown_handler()
    if IS_WEBHOOK:
        await dispatcher.bot.delete_webhook()


def start():
    logging.info(f'Starting in {env.MODE} mode.')
    logging.info(
        f'Connection type: {"webhook" if IS_WEBHOOK else "long-polling"}')
    if IS_WEBHOOK:
        logging.info(f'Webhook: {WEBHOOK_URL}')
        logging.info(f'Port: {WEBAPP_PORT}')

    if handlers:
        logging.info("Handlers attached")
    else:
        logging.error("Handlers NOT attached", handlers)

    options = {
        'dispatcher': dp,
        'on_startup': on_startup_callback,
        'on_shutdown': on_shutdown_callback,
        'skip_updates': True
    }

    if IS_WEBHOOK:
        from aiohttp import web
        start_webhook(
            **options,
            loop=asyncio.get_event_loop(),
            webhook_path=WEBHOOK_PATH,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
            web_app=routes.apply(web.Application())
        )
    else:
        start_polling(
            **options,
        )
