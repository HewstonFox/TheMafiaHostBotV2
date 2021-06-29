import asyncio

from aiogram.types import Message

from bot.controllers.MessaggeController.MessageController import MessageController
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.UserController import collection as user_collection
from bot.controllers.UserController.types import UserRecord
from bot.localization import Localization


class UserController:
    @classmethod
    async def start_user(cls, message: Message, t: Localization):
        user = message.from_user
        if not await user_collection.check_if_user_record_exists(user.id):
            user_record: UserRecord = await user_collection.create_user_record(
                chat_id=user.id,
                full_name=user.full_name,
                username=user.username,
            )
        else:
            user_record: UserRecord = await user_collection.get_user_record_by_chat_id(user.id)

        if user.full_name != user_record['full_name'] or user.username != user_record['username']:
            user_record['full_name'] = user.full_name
            user_record['username'] = user.username
            asyncio.create_task(user_collection.update_user_record(user.id, user_record))

        try:
            session_id = int(message.get_args())
            session = SessionController.get_session(session_id)
            if session.is_user_in(user.id):
                raise ValueError
            session.add_player(user)
        except (ValueError, KeyError):
            await MessageController.send_private_start_message(message.chat.id, t)
