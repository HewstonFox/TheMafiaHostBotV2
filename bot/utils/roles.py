from typing import Dict, Optional, Tuple, Callable

from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType
from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


def valid_player(players: Dict[ChatId, BaseRole], chat_id: ChatId) -> Tuple[Optional[bool], Optional[BaseRole]]:
    id_type = type(chat_id)
    target: Optional[BaseRole] = {id_type(k): v for k, v in players.items()}.get(chat_id)
    if not target:
        return None, None
    return target.alive, target


def get_players_list_menu(role: BaseRole, should_display: Callable[[BaseRole], bool] = lambda x: x.alive) -> dict:
    def get_description(key):
        check_result = valid_player(role.players, key)
        if all(check_result):
            return f'You chose {check_result[1].user.get_mention()}'  # todo: add translation
        return 'This player is not in game'  # todo: add translation

    def select_target(key, _):
        check_result = valid_player(role.players, key)
        if all(check_result):
            role.affect(check_result[1].user.id)
            return True
        return False

    return {
        'chat_id': role.user.id,
        'config': MessageMenu(
            description=f'{role.shortcut} effect',  # todo: add translation
            disable_special_buttons=True,
            buttons=[MessageMenuButton(
                type=ButtonType.endpoint,
                name=pl.user.full_name,
                key=str(pl.user.id)
            ) for pl in role.players.values() if should_display(pl)]
        ),
        'get_data': get_description,
        'set_data': select_target
    }
