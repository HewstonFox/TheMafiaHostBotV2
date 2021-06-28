from bot.controllers.SessionController.Session import Session
from bot.types import ChatId
from bot.bot import bot
from bot.controllers.CallbackQueryController.types import CallbackQueryActions
from bot.utils.message import arr2keyword_markup
from localization import Localization


class MessageController:
    @classmethod
    async def send_private_start_message(cls, chat_id: ChatId, t: Localization):
        inline_keyboard = arr2keyword_markup(
            [[{'text': t.private.button.more, 'callback_data': CallbackQueryActions.more}]])
        return await bot.send_message(chat_id, t.private.start, reply_markup=inline_keyboard)

    @classmethod
    async def send_private_more(cls, chat_id: ChatId, t: Localization):
        return await bot.send_message(chat_id, "Bot`s more, add transition")  # todo add translation

    @classmethod
    async def send_registration_start(cls, chat_id: ChatId, t: Localization):
        inline_keyboard = arr2keyword_markup([[{'text': 'Connect', 'callback_data': CallbackQueryActions.add_player}]])
        return await bot.send_message(chat_id, 'Registration started',
                                      reply_markup=inline_keyboard)  # todo add translation

    @classmethod
    async def send_registration_is_already_started(cls, chat_id: ChatId, t: Localization):
        return await bot.send_message(chat_id, 'Registration is already started')  # todo add translation

    @classmethod
    async def send_registration_reminder(cls, chat_id: ChatId, t: Localization, time: int, reply_id: ChatId):
        inline_keyboard = arr2keyword_markup([[{'text': 'Connect', 'callback_data': CallbackQueryActions.add_player}]])
        return await bot.send_message(chat_id, f'Timer is {time}', reply_markup=inline_keyboard,
                                      reply_to_message_id=reply_id)  # todo add translation

    @classmethod
    async def send_registration_force_stopped(cls, chat_id: ChatId, t: Localization):
        return await bot.send_message(chat_id, 'Registration canceled')  # todo add translation

    @classmethod
    async def send_registration_skipped(cls, chat_id: ChatId, t: Localization):
        return await bot.send_message(chat_id, 'The game was launched ahead of schedule')  # todo add translation

    @classmethod
    async def send_nothing_to_stop(cls, chat_id: ChatId, t: Localization):
        return await bot.send_message(chat_id, 'Nothing to stop')  # todo add translation

    @classmethod
    async def send_user_connected_to_game(cls, chat_id: ChatId, session: Session):
        return await bot.send_message(chat_id, f'You connected to {session.name}')  # todo add translation
