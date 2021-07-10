import io
import traceback

from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, ChatType, Update, ContentType, InputFile
from aiogram.utils.exceptions import BadRequest
from schema import SchemaError

from bot.controllers.GameController.GameController import GameController
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.settings.settings_config import get_settings_menu_config
from bot.controllers.SessionController.types import SessionStatus
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
        await dp.bot.send_message(env.NOTIFICATION_CHAT, f"Error:<code>\n{traceback.format_exc()}</code>")
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
    if session.status == SessionStatus.settings:
        await MenuController.close(session.chat_id)
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
    time = time or session.settings.values['time']['extend']
    await GameController.change_registration_time(session, time, sign)


@throttle_message_handler(commands=['reduce'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def reduce_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    time = time or session.settings.values['time']['reduce']
    await GameController.change_registration_time(session, time, -sign)


@throttle_message_handler(commands=['leave'], chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
async def leave_handler(message: Message, *_, **__):
    await SessionController.leave_user(message.chat.id, message.from_user.id)


@throttle_message_handler(
    filters.CommandSettings(),
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True
)
@clean_command
@with_session
async def settings_handler(msg: Message, session: Session, *_, **__):
    await MenuController.show_menu(session, get_settings_menu_config(session.t), session.settings.get_property,
                                   session.update_settings)


@throttle_message_handler(
    commands=['settings_preset'],
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True
)
@clean_command
@with_session
async def settings_preset_handler(message: Message, session: Session, *_, **__):
    preset = (message.get_args().split()[:1] or [''])[0]
    try:
        session.apply_settings_preset(preset)
    except SchemaError:
        pass
    else:
        # todo: add "preset applied successfully" message in MessageController
        await dp.bot.send_message(message.chat.id, f'Preset <code>{preset}</code> applied successfully')
        pass


@throttle_message_handler(
    commands=['settings_export'],
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True
)
@clean_command
@with_session
async def settings_export_handler(msg: Message, session: Session, *_, **__):
    await dp.bot.send_document(session.chat_id, InputFile(session.settings.export(), 'MafiaHostBotSettings.json'))


@throttle_message_handler(
    Command(['settings_import'], ignore_caption=False),
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True,
    content_types=[ContentType.DOCUMENT],
)
@with_session
async def settings_import_handler(message: Message, session: Session, *_, **__):
    try:
        session.import_settings_from_file(await (await message.document.get_file()).download(destination=io.BytesIO()))
        await message.reply('Got it!')  # todo: add translation
    except SchemaError as e:
        await message.reply(f'Invalid format:\n<code>{e.code}</code>')  # todo: add translation


@dp.message_handler(content_types=[ContentType.PINNED_MESSAGE])
async def clear_pined_by_bot(message: Message):
    username = (await dp.bot.me).username
    if message.from_user.username == username:
        await message.delete()
