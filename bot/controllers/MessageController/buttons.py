from bot.bot import bot
from bot.controllers.CallbackQueryController.types import CallbackQueryActions
from bot.utils.message import arr2keyword_markup


def more(t):
    return arr2keyword_markup([[{'text': t.private.button.more, 'callback_data': CallbackQueryActions.more}]])


def connect(t):
    return arr2keyword_markup([[{'text': t.group.button.connect, 'callback_data': CallbackQueryActions.add_player}]])


def to_bot(t):
    # todo: add translation
    return arr2keyword_markup([[{'text': 'Go to bot', 'url': f'https://t.me/{getattr(bot, "_me").username}'}]])
