import traceback
from pprint import pprint

from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery, Message, ChatType, Update, ContentType
from aiogram.utils.exceptions import BadRequest

from bot.controllers.GameController.GameController import GameController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.settings.Settings import Settings
from bot.controllers.UserController.UserController import UserController
from bot.bot import dp
from bot.controllers.CallbackQueryController.CallbackQueryController import CallbackQueryController
from bot.controllers.MessageController.MessageController import MessageController
from bot.localization import Localization
from bot.utils.decorators.handlers import with_locale, clean_command, with_session
from bot.utils.decorators.throttle import throttle_message_handler, throttle_callback_query_handler
from bot.utils.message import parse_timer
from config import env


@dp.errors_handler()
async def error_handler(update: Update, error: BadRequest):
    try:
        await dp.bot.send_message(env.NOTIFICATION_CHAT, f"Error:<code>\n`{traceback.format_exc()}`</code>")
    except Exception as e:
        print(e)
    print(SessionController._SessionController__sessions)


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
async def leave_handler(message: Message, *_, **__):
    await SessionController.leave_user(message.chat.id, message.from_user.id)


@throttle_message_handler(filters.CommandSettings(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
                          is_chat_admin=True)
@clean_command
@with_session
async def settings_handler(message: Message, session: Session, *_, **__):
    settings = Settings()
    pprint(settings.values)
    print(Settings.validate(settings.values))


@dp.message_handler(content_types=[ContentType.PINNED_MESSAGE])
async def clear_pined_by_bot(message: Message):
    username = (await dp.bot.me).username
    if message.from_user.username == username:
        await message.delete()
