from aiogram.types import CallbackQuery, ChatMemberStatus
from aiogram.utils.exceptions import Unauthorized

from bot.controllers import DispatcherProvider
from bot.controllers.AuthController.AuthController import AuthController
from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.ReactionCounterController.ReactionCounterController import ReactionCounterController
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import UserNotExistsError
from bot.types import ChatId
from bot.utils.shared import raise_if_error
from bot.controllers.UserController import collection as user_collection
from bot.localization import Localization


class CallbackQueryController(DispatcherProvider):

    @classmethod
    async def more(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        await MessageController.send_private_more(chat_id, t)
        return await query.answer()

    @classmethod
    async def add_player(cls, query: CallbackQuery, chat_id: ChatId, t: Localization):
        if not SessionController.is_active_session(chat_id):
            return await query.answer(t.callback_query.session.is_not_active)

        session = SessionController.get_session(chat_id)
        if session.status != SessionStatus.registration:
            return await query.answer(t.callback_query.session.registration_already_ended)

        if len(session.players) == session.settings.values['players']['max']:
            return await query.answer(t.callback_query.session.too_many_players)

        user_id = query.from_user.id
        if session.is_user_in(user_id):
            return await query.answer(t.callback_query.player.already_join)

        try:
            if not await user_collection.check_if_user_record_exists(user_id):
                raise UserNotExistsError
            link = f'<a href="{session.invite_url}">{session.name}</a>'
            res = await MessageController.send_user_connected_to_game(user_id, session.t, link)
            raise_if_error(res)
        except (UserNotExistsError, Unauthorized):
            return await query.answer(url=f'https://t.me/{(await cls.dp.bot.me).username}?start={chat_id}')

        session.add_player(query.from_user)
        return await query.answer(t.callback_query.player.joined)

    @classmethod
    async def apply(cls, query: CallbackQuery, t: Localization):
        key = query.data.split()[0]
        if key == 'menu':
            if query.message.chat.id == query.from_user.id or \
                    ChatMemberStatus.is_chat_admin((await query.message.chat.get_member(query.from_user.id)).status):
                return await MenuController.callback_handler(query)
        if key == 'auth':
            return await AuthController.callback_handler(query, t)
        if key == 'vote':
            if SessionController.is_active_session(query.message.chat.id):
                session = SessionController.get_session(query.message.chat.id)
                if session.status == SessionStatus.game and query.from_user.id not in map(
                        lambda r: r.user.id if r.alive else None, session.roles.values()):
                    return await query.answer(t.callback_query.player.not_allowed)
            return await ReactionCounterController.callback_handler(query)
        if key in cls.__dict__:
            return await getattr(cls, key)(query, query.message.chat.id, t)
        else:
            return await query.answer()
