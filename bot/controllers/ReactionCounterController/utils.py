import asyncio
from typing import Optional

from aiogram.types import Message, User

from bot.controllers.ReactionCounterController.config import chunk_size
from bot.controllers.ReactionCounterController.types import Reactions
from bot.utils.message import arr2keyword_markup
from bot.utils.shared import chunks


def generate_rerender_subscriber(message: Message, text: str = None):
    def subscriber(reactions: Reactions):
        asyncio.create_task(message.edit_text(text or message.text, reply_markup=create_reaction_keyboard(reactions)))

    return subscriber


def create_reaction_keyboard(reactions: Reactions):
    return arr2keyword_markup([[{
        'text': f'{reaction[0]} ({len(reaction[1])})',
        'callback_data': f'vote {reaction[0]}'
    } for reaction in chunk] for chunk in chunks(reactions.items(), chunk_size)])


def find_reaction_member(reactions: Reactions, member: User) -> Optional[str]:
    for reaction, members in reactions.items():
        if member.id in map(lambda m: m.id, members):
            return reaction


def generate_reactions_result_text(text: str, reactions: Reactions):
    return text + '\n\n' + '\n'.join(
        map(lambda r: f'{r[0]} ({len(r[1])})', reactions.items()))
