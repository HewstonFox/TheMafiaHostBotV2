from typing import Optional

from aiogram.types import Message, User, CallbackQuery

from bot.controllers import DispatcherProvider
from bot.controllers.ReactionCounterController.types import Reactions
from bot.controllers.ReactionCounterController.utils import create_reaction_keyboard, generate_rerender_subscriber, \
    generate_reactions_result_text, find_reaction_member
from bot.types import ChatId, Proxy


class ReactionCounterMessage(DispatcherProvider):
    def __init__(
            self,
            chat_id: ChatId,
            text: str,
            reactions: list[str],
            multiply: bool = False,
            accept_ids: list[ChatId] = (),
            exclude_ids: list[ChatId] = ()
    ):
        self.text: str = text
        self.reactions: Reactions = Proxy({reaction: [] for reaction in reactions})
        self.multiply: bool = multiply
        self.chat_id: ChatId = chat_id
        self.accept_ids: list[ChatId] = accept_ids
        self.exclude_ids: list[ChatId] = exclude_ids
        self.msg: Optional[Message] = None

    async def send(self):
        self.msg = await self.dp.bot.send_message(
            self.chat_id,
            self.text,
            reply_markup=create_reaction_keyboard(self.reactions)
        )
        self.reactions.subscribe(generate_rerender_subscriber(self.msg, self.text))

    async def stop(self):
        if not self.msg:
            return

        self.reactions.unsubscribe_all()
        await self.msg.edit_text(generate_reactions_result_text(self.text, self.reactions))

    async def callback_handler(self, reaction: str, user: User, query: CallbackQuery):
        current_reaction = find_reaction_member(self.reactions, user)
        reactions = self.reactions

        await query.answer()

        if self.accept_ids and user.id not in self.accept_ids:
            return

        if self.exclude_ids and user.id in self.exclude_ids:
            return

        if current_reaction == reaction:
            reactions[current_reaction] = list(filter(lambda m: m.id != user.id, reactions[reaction]))
        elif self.multiply or not current_reaction:
            reactions[reaction] = [*reactions[reaction], user]
        else:
            # optimization: append operation will not trigger proxy subscribers, it is needed to update message once
            reactions[reaction].append(user)
            reactions[current_reaction] = list(filter(lambda m: m.id != user.id, reactions[current_reaction]))
