from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class LPrivateButton(DataclassFromDict):
    more: str = field_from_dict()


@dataclass
class LPrivate(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()
    more_description: str = field_from_dict()
    user_connected: str = field_from_dict()
    user_left: str = field_from_dict()
    button: LPrivateButton = field_from_dict()
