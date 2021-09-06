import asyncio
from typing import Callable, Any, Optional
import logging

from aiogram.types import User, Message, CallbackQuery

from bot.controllers import BaseController
from bot.controllers.ReactionCounterController.config import chunk_size
from bot.types import ChatId, Proxy
from bot.utils.message import arr2keyword_markup
from bot.utils.shared import chunks, flat_list

Reactions = Proxy[str, list[User]]


class ReactionCounterController(BaseController):
    __active_reactions: dict[str, (Reactions, bool)] = {}

    @classmethod
    async def callback_handler(cls, query: CallbackQuery):
        reaction = query.data.split()[1]
        message = query.message

        active_reaction = cls.__active_reactions.get(f'{message.chat.id} {message.message_id}')
        if not active_reaction:
            await cls.close_reaction_counting(message)
            return

        reactions, multiply = active_reaction

        if reaction not in reactions:
            return

        user = query.from_user
        current_reaction = cls.find_reaction_member(reactions, user)

        if current_reaction == reaction:
            reactions[current_reaction] = list(filter(lambda m: m.id != user.id, reactions[reaction]))
            return

        if multiply or not current_reaction:
            reactions[reaction] = reactions[reaction] + [user]
            return

        # optimization: follow operation will not trigger proxy subscribers, it is need to update message once
        reactions[reaction].append(user)
        reactions[current_reaction] = list(filter(lambda m: m.id != user.id, reactions[reaction]))

    @classmethod
    async def send_reaction_counter(cls,
                                    chat_id: ChatId,
                                    message: str,
                                    reactions: list[str],
                                    multiply: bool = False,
                                    *
                                    timeout: Optional[int],
                                    callback: Optional[Callable[[Reactions], Any]] = None
                                    ):
        if callback and timeout is None:
            logging.warning('Callback will never be called because of infinite result counting')

        reactions_dict: Reactions = Proxy({reaction: [] for reaction in reactions})

        msg = await cls.dp.bot.send_message(chat_id, message, reply_markup=cls.create_reaction_keyboard(reactions_dict))

        reactions_dict.subscribe(cls.generate_rerender_subscriber(msg))

        cls.__active_reactions[f'{chat_id} {msg.message_id}'] = reactions_dict, multiply

        return msg

    @classmethod
    def create_reaction_keyboard(cls, reactions: Reactions):
        return arr2keyword_markup([[{
            'text': f'{reaction[0]} - {len(reaction[1])}',
            'callback_data': f'vote {reaction[0]}'
        } for reaction in chunk] for chunk in chunks(reactions.items(), chunk_size)])

    @classmethod
    def generate_rerender_subscriber(cls, message: Message):
        def subscriber(reactions: Reactions):
            asyncio.create_task(message.edit_text(message.text, reply_markup=cls.create_reaction_keyboard(reactions)))

        return subscriber

    @classmethod
    async def close_reaction_counting(cls, message: Message, reactions: Optional[Reactions] = None):
        if not reactions:
            reactions = Proxy(
                {button.text.split()[0]: button.text.split()[2] for button in
                 flat_list(message.reply_markup.inline_keyboard)})

        reactions.unsubscribe_all()

        cls.__active_reactions.pop(f'{message.chat.id} {message.message_id}', None)
        print(list(map(lambda r: f'{r[0]} - {r[1]}', reactions.items())))
        await message.edit_text(message.text + '\n\n' + '\n'.join(
            map(lambda r: f'{r[0]} - {r[1] if isinstance(r[1], int) else len(r[1])}', reactions.items())))

    @classmethod
    def find_reaction_member(cls, reactions: Reactions, member: User) -> Optional[str]:
        for reaction, members in reactions.items():
            if member.id in map(lambda m: m.id, members):
                return reaction
