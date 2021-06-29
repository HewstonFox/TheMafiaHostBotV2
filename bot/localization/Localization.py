from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class PrivateButton(DataclassFromDict):
    more: str = field_from_dict()


@dataclass
class Private(DataclassFromDict):
    start: str = field_from_dict()
    button: PrivateButton = field_from_dict()


@dataclass
class Localization(DataclassFromDict):
    Locale: str = field_from_dict()
    language: str = field_from_dict()
    private: Private = field_from_dict()
