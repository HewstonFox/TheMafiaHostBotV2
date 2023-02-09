from functools import reduce
import asyncio
from typing import Dict, Optional, Tuple, Callable, Coroutine
import re

from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId
from bot.utils.emoji_strings import get_role_name


def valid_player(
        players: Dict[ChatId, 'BaseRole'],
        chat_id: ChatId
) -> Tuple[Optional[bool], Optional['BaseRole'], Optional[bool]]:
    id_type = type(chat_id)
    target: Optional['BaseRole'] = {id_type(k): v for k, v in players.items()}.get(chat_id)
    if not target:
        return False, None, False
    return target.alive, target, target.session.is_night


def get_description_factory(players: Dict[ChatId, 'BaseRole'], role: 'BaseRole', night_action=True):
    def get_description(key):
        if not role.alive:
            return role.t.callback_query.player.already_dead
        chat_id = (re.findall(r'\d+', key) or [0])[0]
        alive, target, is_night = valid_player(players, chat_id)
        if alive and target and night_action == is_night:
            return role.t.callback_query.player.choose_target.format(target.user.get_mention())
        return role.t.callback_query.player.not_allowed

    return get_description


def select_target_factory(players: Dict[ChatId, 'BaseRole'], role: 'BaseRole', night_action=True, method='affect'):
    def select_target(key, _):
        chat_id = (re.findall(r'\d+', key) or [0])[0]
        alive, target, is_night = valid_player(players, chat_id)
        if alive and target:
            if night_action != is_night or not role.alive:
                return True
            task = getattr(role, method)(target.user.id, key)
            if isinstance(task, Coroutine):
                asyncio.create_task(task)
            return True
        return False

    return select_target


def players_list_menu_factory(
        description: str,
        roles: list['BaseRole'],
        should_display: Callable[['BaseRole'], bool] = lambda x: x.alive
):
    return MessageMenu(
        description=description,
        disable_special_buttons=True,
        buttons=[MessageMenuButton(
            type=ButtonType.endpoint,
            name=pl.user.full_name,
            key=str(pl.user.id)
        ) for pl in roles if should_display(pl)]
    )


def get_players_list_menu(role: 'BaseRole', should_display: Callable[['BaseRole'], bool] = None) -> dict:
    return {
        'chat_id': role.user.id,
        'config': players_list_menu_factory(
            getattr(role.t.roles, role.shortcut).effect,
            list(role.players.values()),
            should_display
        ),
        'get_data': get_description_factory(role.players, role),
        'set_data': select_target_factory(role.players, role),
        't': role.t
    }


def get_roles_list(roles: list[BaseRole]) -> str:
    return reduce(
        lambda acc, role: acc + f'    {role.user.get_mention()} - {get_role_name(role.shortcut, role.t)}\n',
        roles, ''
    )
