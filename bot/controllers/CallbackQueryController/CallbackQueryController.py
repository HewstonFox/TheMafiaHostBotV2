from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import Unauthorized

from bot.bot import bot
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import UserNotExistsError
from bot.types import ChatId
from bot.utils.shared import raise_if_error
from bot.controllers.UserController import collection as user_collection
from bot.localization import Localization


class CallbackQueryController:
    @classmethod
    async def more(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        await MessageController.send_private_more(chat_id, t)
        await query.answer()

    @classmethod
    async def add_player(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        if not SessionController.is_active_session(chat_id):
            await query.answer(text='Session is not active')  # todo add translation
            return

        session = SessionController.get_session(chat_id)
        if session.status != SessionStatus.registration:
            await query.answer(text='Session is registration')  # todo add translation
            return

        # todo add to many players check

        user_id = query.from_user.id
        if session.is_user_in(user_id):
            await query.answer(text='You are already in session')  # todo add translation
            return

        try:
            if not await user_collection.check_if_user_record_exists(user_id):
                raise UserNotExistsError
            res = await MessageController.send_user_connected_to_game(user_id, session)
            raise_if_error(res)
        except (UserNotExistsError, Unauthorized):
            await query.answer(url=f'https://t.me/{(await bot.me).username}?start={chat_id}')
            return

        session.add_player(query.from_user)
        await query.answer(text="You Successfully connected")  # todo add translation

    @classmethod
    async def apply(cls, query: CallbackQuery, t: Localization):
        return await getattr(cls, query.data.split()[0])(query, query.message.chat.id, t)
