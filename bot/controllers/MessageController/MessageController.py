from typing import List

from aiogram import Dispatcher

from bot.controllers.MessageController import buttons
from bot.types import ChatId
from bot.controllers.SessionController.Session import Session
from bot.localization import Localization


class MessageController:
    dp: Dispatcher

    @classmethod
    async def cleanup_messages(cls, chat_id: ChatId, ids: List[ChatId]):
        for msg_id in ids:
            await cls.dp.bot.delete_message(chat_id, msg_id)

    @classmethod
    async def send_private_start_message(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.private.start, reply_markup=buttons.more(t))

    @classmethod
    async def send_private_more(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.private.more_description)

    @classmethod
    async def send_registration_start(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(
            chat_id,
            t.group.registration.start.format(''),
            reply_markup=buttons.connect(t)
        )

    @classmethod
    async def update_registration_start(cls, chat_id: ChatId, message_id: int, session: Session):
        players = ', '.join(map(lambda x: x.get_mention(), session.players.values()))
        res = await cls.dp.bot.edit_message_text(
            text=session.t.group.registration.start.format(players),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=buttons.connect(session.t),
        )
        return res

    @classmethod
    async def send_registration_is_already_started(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.already_started)

    @classmethod
    async def send_registration_reminder(cls, chat_id: ChatId, t: Localization, time: int, reply_id: ChatId):
        return await cls.dp.bot.send_message(
            chat_id, t.group.registration.reminder.format(time),
            reply_markup=buttons.connect(t),
            reply_to_message_id=reply_id
        )

    @classmethod
    async def send_registration_force_stopped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.force_stopped)

    @classmethod
    async def send_registration_skipped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.skipped)

    @classmethod
    async def send_registration_reduced(cls, chat_id: ChatId, t: Localization, delta: int, time: int):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.reduced.format(delta, time))

    @classmethod
    async def send_registration_extended(cls, chat_id: ChatId, t: Localization, delta: int, time: int):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.extended.format(delta, time))

    @classmethod
    async def send_nothing_to_stop(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_nothing_to_reduce(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_nothing_to_extend(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_user_connected_to_game(cls, chat_id: ChatId, session: Session):
        return await cls.dp.bot.send_message(chat_id, session.t.private.user_connected.format(session.name))

    @classmethod
    async def send_user_left_game(cls, chat_id: ChatId, session: Session):
        return await cls.dp.bot.send_message(chat_id, session.t.private.user_left.format(session.name))
