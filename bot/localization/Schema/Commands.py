from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class LPrivateCommands(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()


@dataclass
class LGroupCommands(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()
    game: str = field_from_dict()
    reduce: str = field_from_dict()
    extend: str = field_from_dict()
    leave: str = field_from_dict()
    settings: str = field_from_dict()
    stop: str = field_from_dict()


@dataclass
class LCommands(DataclassFromDict):
    private: LPrivateCommands = field_from_dict()
    group: LGroupCommands = field_from_dict()
