from typing import Dict, Optional, Tuple

from bot.models.Roles.BaseRole import BaseRole
from bot.types import ChatId


def valid_player(players: Dict[ChatId, BaseRole], chat_id: ChatId) -> Tuple[Optional[bool], Optional[BaseRole]]:
    id_type = type(chat_id)
    target: Optional[BaseRole] = {id_type(k): v for k, v in players.items()}.get(chat_id)
    if not target:
        return None, None
    return target.alive, target
