from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery, Message, ChatType

from bot.controllers.GameController.GameController import GameController
from bot.controllers.SessionController.SessionController import SessionController
from bot.utils.decorators import with_locale
from bot.bot import dp
from bot.controllers.CallbackQueryController.CallbackQueryController import CallbackQueryController
from bot.controllers.MessaggeController.MessageController import MessageController
from localization import Localization, get_translation


@dp.callback_query_handler()
@with_locale
async def callback_query_handler(query: CallbackQuery, t: Localization):
    await CallbackQueryController.apply(query, t)


@dp.message_handler(filters.CommandStart(), chat_type=ChatType.PRIVATE)
@with_locale
async def private_start_handler(message: Message, t: Localization):
    await MessageController.send_private_start_message(message.chat.id, t)


@dp.message_handler(filters.CommandHelp(), chat_type=ChatType.PRIVATE)
@with_locale
async def private_help_handler(message: Message, t: Localization):
    await MessageController.send_private_more(message.chat.id, t)


@dp.message_handler(filters.CommandStart(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def group_start_handler(message: Message):
    await message.reply('U wrote start in group')


@dp.message_handler(commands=['game'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    t = get_translation('en')
    await GameController.run_new_game(message.chat.id, t)


@dp.message_handler(commands=['stop'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    t = get_translation('en')
    await GameController.force_stop(message.chat.id, t)


@dp.message_handler(commands=['extend'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    await message.reply('U wrote extend')


@dp.message_handler(commands=['reduce'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    await message.reply('U wrote reduce')


@dp.message_handler(commands=['leave'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    await message.reply('U wrote leave')


@dp.message_handler(commands=['settings'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def start_handler(message: Message):
    await message.reply('U wrote settings')