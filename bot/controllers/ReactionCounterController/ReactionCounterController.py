from aiogram.types import Message, CallbackQuery

from bot.controllers import DispatcherProvider
from bot.controllers.ReactionCounterController.ReactionCounterMessage import ReactionCounterMessage
from bot.types import ChatId


class ReactionCounterController(DispatcherProvider):
    __active_reactions_messages: dict[str, ReactionCounterMessage] = {}

    @classmethod
    async def callback_handler(cls, query: CallbackQuery):
        reaction = query.data.split()[1]
        message = query.message

        reaction_message = cls.__active_reactions_messages.get(f'{message.chat.id} {message.message_id}')
        if not reaction_message:
            await cls.stop_reaction_counter(message=message)
            await query.answer()
            return

        await reaction_message.callback_handler(reaction, query.from_user, query)

    @classmethod
    async def send_reaction_counter(
            cls,
            chat_id: ChatId,
            message: str,
            reactions: list[str],
            multiply: bool = False,
            accept_ids: list[ChatId] = [],
            exclude_ids: list[ChatId] = []
    ) -> ReactionCounterMessage:
        reaction_message = ReactionCounterMessage(chat_id, message, reactions, multiply, accept_ids, exclude_ids)
        await reaction_message.send()
        cls.__active_reactions_messages[f'{chat_id} {reaction_message.msg.message_id}'] = reaction_message
        return reaction_message

    @classmethod
    async def stop_reaction_counter(cls, *, message: Message = None, reaction_counter: ReactionCounterMessage = None):
        if message:
            await message.delete()
        if reaction_counter:
            cls.__active_reactions_messages.pop(f'{reaction_counter.chat_id} {reaction_counter.msg.message_id}', None)
            await reaction_counter.stop()
