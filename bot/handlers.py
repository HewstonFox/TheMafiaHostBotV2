from aiogram.dispatcher import filters
from aiogram.types import CallbackQuery, Message, ChatType
from aiogram.utils.exceptions import Throttled

from bot.controllers.GameController.GameController import GameController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.UserController.UserController import UserController
from bot.utils.decorators import with_locale, with_session, clean_command
from bot.bot import dp
from bot.controllers.CallbackQueryController.CallbackQueryController import CallbackQueryController
from bot.controllers.MessageController.MessageController import MessageController
from bot.localization import Localization
from bot.utils.message import parse_timer


@dp.callback_query_handler()
@with_locale
async def callback_query_handler(query: CallbackQuery, t: Localization):
    await CallbackQueryController.apply(query, t)


@dp.message_handler(filters.CommandStart(), chat_type=ChatType.PRIVATE)
@clean_command
@with_locale
async def private_start_handler(message: Message, t: Localization):
    await UserController.start_user(message, t)


@dp.message_handler(filters.CommandHelp(), chat_type=ChatType.PRIVATE)
@clean_command
@with_locale
async def private_help_handler(message: Message, t: Localization):
    await MessageController.send_private_more(message.chat.id, t)


@dp.message_handler(filters.CommandStart(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def group_start_handler(message: Message, session: Session):
    await message.bot.send_message(message.chat.id, 'U wrote start in group')


@dp.message_handler(commands=['game'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def game_handler(message: Message, session: Session):
    try:
        await dp.throttle('game', rate=2, chat_id=session.chat_id)
    except Throttled:
        await message.bot.send_message(session.chat_id, 'hold on!')
    else:
        time, sign = parse_timer(message.text)
        await GameController.run_new_game(session, time)


@dp.message_handler(commands=['stop'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def stop_handler(_: Message, session: Session):
    await GameController.force_stop(session)


@dp.message_handler(commands=['extend'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def extend_handler(message: Message, session: Session):
    time, sign = parse_timer(message.text)
    await GameController.change_registration_time(session, time, sign)


@dp.message_handler(commands=['reduce'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def reduce_handler(message: Message, session: Session):
    time, sign = parse_timer(message.text)
    await GameController.change_registration_time(session, time, -sign)


@dp.message_handler(commands=['leave'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
async def leave_handler(message: Message):
    await SessionController.leave_user(message.chat.id, message.from_user.id)


@dp.message_handler(filters.CommandSettings(), chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], is_chat_admin=True)
@clean_command
@with_session
async def settings_handler(message: Message, session: Session):
    await message.reply('U wrote settings')


@dp.message_handler(commands=['sessions'])
async def sessions_handler(message):
    print(SessionController._SessionController__sessions)
