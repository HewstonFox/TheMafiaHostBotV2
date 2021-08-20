from asyncio import create_task
from typing import Dict, Optional, Tuple, Callable
import re

from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


def valid_player(players: Dict[ChatId, 'BaseRole'], chat_id: ChatId) -> Tuple[Optional[bool], Optional['BaseRole']]:
    id_type = type(chat_id)
    target: Optional['BaseRole'] = {id_type(k): v for k, v in players.items()}.get(chat_id)
    if not target:
        return None, None
    return target.alive, target


def get_description_factory(players: Dict[ChatId, 'BaseRole']):
    def get_description(key):
        chat_id = (re.findall(r'\d+', key) or [0])[0]
        check_result = valid_player(players, chat_id)
        if all(check_result):
            return f'You chose {check_result[1].user.get_mention()}'  # todo: add translation
        return 'This player is not in game'  # todo: add translation

    return get_description


def select_target_factory(players: Dict[ChatId, 'BaseRole'], role: 'BaseRole'):
    def select_target(key, _):
        chat_id = (re.findall(r'\d+', key) or [0])[0]
        check_result = valid_player(players, chat_id)
        if all(check_result):
            create_task(role.affect(check_result[1].user.id, key))
            return True
        return False

    return select_target


def players_list_menu_factory(
        description: str,
        roles: list['BaseRole'],
        should_display: Callable[['BaseRole'], bool] = lambda x: x.alive
):
    return MessageMenu(
        description=description,  # todo: add translation
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
            f'{role.shortcut} effect',  # todo: add translation,
            list(role.players.values()),
            should_display
        ),
        'get_data': get_description_factory(role.players),
        'set_data': select_target_factory(role.players, role)
    }
