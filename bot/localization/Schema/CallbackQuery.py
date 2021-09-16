from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class LSession(DataclassFromDict):
    is_not_active: str = field_from_dict()
    registration_already_ended: str = field_from_dict()
    too_many_players: str = field_from_dict()


@dataclass
class LPlayer(DataclassFromDict):
    already_join: str = field_from_dict()
    joined: str = field_from_dict()
    not_allowed: str = field_from_dict()
    choose_target: str = field_from_dict()
    already_dead: str = field_from_dict()


@dataclass
class LCallbackQuery(DataclassFromDict):
    session: LSession = field_from_dict()
    player: LPlayer = field_from_dict()
