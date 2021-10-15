from bot.emoji import emoji
from bot.localization import Localization


def get_role_name(shortcut: str, t: Localization) -> str:
    return f'{getattr(emoji.role, shortcut)}{getattr(t.roles, shortcut).name}'


def get_action_message(shortcut: str, t: Localization):
    return f'{getattr(emoji.action, shortcut)} {getattr(t.roles, shortcut).affect}'


def get_global_action_message(shortcut: str, t: Localization):
    return f'{getattr(emoji.action, shortcut)} {getattr(t.roles, shortcut).global_effect}'
