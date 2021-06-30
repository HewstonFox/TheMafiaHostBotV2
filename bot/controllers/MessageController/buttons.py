from bot.controllers.CallbackQueryController.types import CallbackQueryActions
from bot.utils.message import arr2keyword_markup


def more(t):
    return arr2keyword_markup([[{'text': t.private.button.more, 'callback_data': CallbackQueryActions.more}]])


def connect(t):
    return arr2keyword_markup([[{'text': t.group.button.connect, 'callback_data': CallbackQueryActions.add_player}]])
