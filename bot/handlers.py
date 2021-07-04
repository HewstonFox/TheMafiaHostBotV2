from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery, Message, ChatType

from bot.controllers.GameController.GameController import GameController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.UserController.UserController import UserController
from bot.bot import dp
from bot.controllers.CallbackQueryController.CallbackQueryController import CallbackQueryController
from bot.controllers.MessageController.MessageController import MessageController
from bot.localization import Localization
from bot.utils.decorators.handlers import with_locale, clean_command, with_session
from bot.utils.decorators.throttle import throttle_message_handler, throttle_callback_query_handler
from bot.utils.message import parse_timer


@throttle_callback_query_handler()
@with_locale
async def callback_query_handler(query: CallbackQuery, t: Localization, *_, **__):
    await CallbackQueryController.apply(query, t)


@throttle_message_handler(filters.CommandStart(), chat_type=ChatType.PRIVATE)
@clean_command
@with_locale
async def private_start_handler(message: Message, t: Localization, *_, **__):
    await UserController.start_user(message, t)


@throttle_message_handler(filters.CommandHelp(), chat_type=ChatType.PRIVATE)
@clean_command
@with_locale
async def private_help_handler(message: Message, t: Localization, *_, **__):
    await MessageController.send_private_more(message.chat.id, t)


@throttle_message_handler(filters.CommandStart(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def group_start_handler(message: Message, session: Session, *_, **__):
    await message.bot.send_message(message.chat.id, 'U wrote start in group')


@throttle_message_handler(commands=['game'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def game_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    await GameController.run_new_game(session, time)


@throttle_message_handler(commands=['stop'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def stop_handler(msg: Message, session: Session, *_, **__):
    await GameController.force_stop(session)


@throttle_message_handler(commands=['extend'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def extend_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    await GameController.change_registration_time(session, time, sign)


@throttle_message_handler(commands=['reduce'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def reduce_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    await GameController.change_registration_time(session, time, -sign)


@throttle_message_handler(commands=['leave'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
async def leave_handler(message: Message):
    await SessionController.leave_user(message.chat.id, message.from_user.id)


@throttle_message_handler(filters.CommandSettings(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
                          is_chat_admin=True)
@clean_command
@with_session
async def settings_handler(message: Message, session: Session, *_, **__):
    await message.reply('U wrote settings')


# todo: remove, just for debug
@dp.message_handler(commands=['sessions'])
async def sessions_handler(message):
    print(SessionController._SessionController__sessions)
