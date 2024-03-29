import io
import json
from asyncio import sleep

from aiogram.dispatcher.webhook import SendMessage
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, ChatType, Update, ContentType, \
    InputFile
from aiogram.utils.exceptions import BadRequest
from schema import SchemaError

from bot.constants import WEBHOOK_HOST, TELEGRAM_MESSAGE_MAX_SIZE
from bot.controllers.ErrorController.ErrorController import ErrorController
from bot.controllers.GameController.GameController import GameController
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.ReactionCounterController.ReactionCounterController import \
    ReactionCounterController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import \
    SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.controllers.UserController.UserController import UserController
from bot.bot import dp
from bot.controllers.CallbackQueryController.CallbackQueryController import \
    CallbackQueryController
from bot.controllers.MessageController.MessageController import \
    MessageController
from bot.localization import Localization
from bot.utils.decorators.handlers import with_locale, clean_command, \
    with_session
from bot.utils.decorators.throttle import throttle_message_handler, \
    throttle_callback_query_handler
from bot.utils.filters import ForwardFromMe
from bot.utils.message import parse_timer
from bot.utils.shared import batch_str
from config import env


@dp.errors_handler()
async def error_handler(update: Update, error: BadRequest):
    print('UPDATE:', update.update_id)
    context = {
        'update': update.to_python(),
    }

    session = SessionController.get_session(update.message.chat.id)
    if session:
        context['session'] = session.get_dump()

    error_record = ErrorController.add_error(error, context)

    if not WEBHOOK_HOST:
        ErrorController.remove_error(error_record['id'])

        error_json = json.dumps(error_record, indent=2)
        print(error_json)
        for msg in batch_str(error_json, TELEGRAM_MESSAGE_MAX_SIZE):
            await dp.bot.send_message(env.NOTIFICATION_CHAT,
                                      f'<code>{msg}</code>')
        return

    return SendMessage(
        env.NOTIFICATION_CHAT,
        f'Error: <a href="{WEBHOOK_HOST}/app/private/errors?error={error_record["id"]}">Link</a>'
    )


@dp.message_handler(
    commands=['session'],
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    user_id=env.NOTIFICATION_CHAT
)
@clean_command
@with_session
async def current_session(message: Message, session: Session, *_, **__):
    await dp.bot.send_message(
        env.NOTIFICATION_CHAT,
        f'Session: \n'
        f'Name: {session.name}\n'
        f'Status: {session.status}\n'
        f'Chat Id: {session.chat_id}\n'
        f'Invite url: {session.invite_url}\n'
        f'Players: {", ".join(map(lambda u: u.mention, session.players.values()))}'
        f'\n'
        f'Message id: {message.message_id}\n'
        f''
    )
    print(json.dumps(session.get_dump(), indent=2,
                     default=lambda x: x.get_dump()))


@throttle_callback_query_handler()
@with_locale
async def callback_query_handler(query: CallbackQuery, t: Localization, *_,
                                 **__):
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
    await MessageController.send_private_help_message(message.chat.id, t)


@throttle_message_handler(filters.CommandHelp(),
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_locale
async def private_help_handler(message: Message, t: Localization, *_, **__):
    await MessageController.send_group_help_message(message.chat.id, t)


@throttle_message_handler(filters.CommandStart(),
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def group_start_handler(message: Message, session: Session, *_, **__):
    if session.status in (SessionStatus.registration, SessionStatus.game):
        await GameController.force_start(session)
    else:
        await MessageController.send_group_start_message(session.chat_id,
                                                         session.t)


@throttle_message_handler(commands=['game'],
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def game_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    await MenuController.close(session.chat_id)
    await GameController.run_new_game(session, time)


@throttle_message_handler(commands=['stop'],
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def stop_handler(msg: Message, session: Session, *_, **__):
    await GameController.force_stop(session)


@throttle_message_handler(commands=['extend'],
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def extend_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    time = time or session.settings.values['time']['extend']
    await GameController.change_registration_time(session, time, sign)


@throttle_message_handler(commands=['reduce'],
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
@clean_command
@with_session
async def reduce_handler(message: Message, session: Session, *_, **__):
    time, sign = parse_timer(message.text)
    time = time or session.settings.values['time']['reduce']
    await GameController.change_registration_time(session, time, -sign)


@throttle_message_handler(commands=['leave'],
                          chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
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
    await session.show_settings_menu()


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
        await MessageController.send_preset_apply_success(session.chat_id,
                                                          session.t, preset)


@throttle_message_handler(
    commands=['settings_export'],
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True
)
@clean_command
@with_session
async def settings_export_handler(msg: Message, session: Session, *_, **__):
    await dp.bot.send_document(session.chat_id,
                               InputFile(session.settings.export(),
                                         'MafiaHostBotSettings.json'))


@throttle_message_handler(
    Command(['settings_import'], ignore_caption=False),
    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    is_chat_admin=True,
    content_types=[ContentType.DOCUMENT],
)
@with_session
async def settings_import_handler(message: Message, session: Session, *_, **__):
    try:
        session.import_settings_from_file(
            await (await message.document.get_file()).download(
                destination=io.BytesIO()))
        await message.reply(session.t.group.settings_apply_success)
    except SchemaError as e:
        await message.reply(
            session.t.group.settings_apply_failure.format(e.code))


@dp.message_handler(content_types=[ContentType.PINNED_MESSAGE])
async def clear_pined_by_bot(message: Message):
    username = (await dp.bot.me).username
    if message.from_user.username == username:
        await message.delete()


if env.MODE != 'development':
    @dp.message_handler(ForwardFromMe,
                        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
    @with_session
    async def forward_from_bot(msg: Message, session: Session, *_, **__):
        if session.status == SessionStatus.game:
            await msg.delete()

if env.MODE == 'development':
    @dp.message_handler(commands=['vote'],
                        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
    @clean_command
    async def send_agree(message: Message):
        vote_msg = await ReactionCounterController.send_reaction_counter(
            message.chat.id, 'Lynch somebody',
            ['👍', '👎'], False)
        await sleep(60)
        await ReactionCounterController.stop_reaction_counter(
            reaction_counter=vote_msg)
        print(vote_msg.reactions)


    @dp.message_handler(commands=['error'])
    @clean_command
    async def throw_error(message: Message):
        raise Exception('Synthetic error')
