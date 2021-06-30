from typing import List

from aiogram import Dispatcher

from bot.controllers.SessionController.types import PlayersList
from bot.types import ChatId
from bot.controllers.CallbackQueryController.types import CallbackQueryActions
from bot.controllers.SessionController.Session import Session
from bot.utils.message import arr2keyword_markup
from bot.localization import Localization


class MessageController:
    dp: Dispatcher

    @classmethod
    async def cleanup_messages(cls, chat_id: ChatId, ids: List[ChatId]):
        for msg_id in ids:
            await cls.dp.bot.delete_message(chat_id, msg_id)

    @classmethod
    async def send_private_start_message(cls, chat_id: ChatId, t: Localization):
        inline_keyboard = arr2keyword_markup(
            [[{'text': t.private.button.more, 'callback_data': CallbackQueryActions.more}]])
        return await cls.dp.bot.send_message(chat_id, t.private.start, reply_markup=inline_keyboard)

    @classmethod
    async def send_private_more(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.private.more_description)

    @classmethod
    async def send_registration_start(cls, chat_id: ChatId, t: Localization):
        inline_keyboard = arr2keyword_markup([[{'text': 'Connect', 'callback_data': CallbackQueryActions.add_player}]])
        return await cls.dp.bot.send_message(chat_id, t.group.registration.start, reply_markup=inline_keyboard)

    @classmethod
    async def update_registration_start(cls, chat_id: ChatId, message_id: int, players: PlayersList):
        return

    @classmethod
    async def send_registration_is_already_started(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.already_started)

    @classmethod
    async def send_registration_reminder(cls, chat_id: ChatId, t: Localization, time: int, reply_id: ChatId):
        inline_keyboard = arr2keyword_markup([[{'text': 'Connect', 'callback_data': CallbackQueryActions.add_player}]])
        return await cls.dp.bot.send_message(chat_id, t.group.registration.reminder.format(time),
                                             reply_markup=inline_keyboard,
                                             reply_to_message_id=reply_id)

    @classmethod
    async def send_registration_force_stopped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.force_stopped)

    @classmethod
    async def send_registration_skipped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.skipped)

    @classmethod
    async def send_nothing_to_stop(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_user_connected_to_game(cls, chat_id: ChatId, session: Session):
        return await cls.dp.bot.send_message(chat_id, session.t.private.user_connected.format(session.name))

    @classmethod
    async def send_user_left_game(cls, chat_id: ChatId, session: Session):
        return await cls.dp.bot.send_message(chat_id, session.t.private.user_left.format(session.name))
