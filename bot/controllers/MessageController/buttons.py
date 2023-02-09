from bot.bot import bot
from bot.controllers.CallbackQueryController.types import CallbackQueryActions
from bot.localization import Localization
from bot.utils.message import arr2keyword_markup


def more(t: Localization):
    return arr2keyword_markup([
        [{'text': t.private.button.more, 'url': t.group.telegraph_url}],
        [{'text': t.private.button.add_to_group, 'url': f'https://t.me/{getattr(bot, "_me").username}?startgroup=_'}]
    ])


def connect(t: Localization):
    return arr2keyword_markup([[{'text': t.group.button.connect, 'callback_data': CallbackQueryActions.add_player}]])


def to_bot(t: Localization):
    return arr2keyword_markup(
        [[{'text': t.group.button.go_to_bot, 'url': f'https://t.me/{getattr(bot, "_me").username}'}]])


def auth_request(t: Localization, source: str):
    return arr2keyword_markup([[
        {'text': t.auth.options.confirm, 'callback_data': f'auth + {source}'},
        {'text': t.auth.options.reject, 'callback_data': f'auth - {source}'},
    ]])
