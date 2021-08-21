from aiogram.types import Message

from bot.bot import bot


def ForwardFromMe(msg: Message):
    if not msg.forward_from or msg.forward_from.id != bot.id:
        return False
    return True
