from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class PrivateButton(DataclassFromDict):
    more: str = field_from_dict()


@dataclass
class Private(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()
    more_description: str = field_from_dict()
    user_connected: str = field_from_dict()
    user_left: str = field_from_dict()
    button: PrivateButton = field_from_dict()


@dataclass
class Registration(DataclassFromDict):
    start: str = field_from_dict()
    already_started: str = field_from_dict()
    reminder: str = field_from_dict()
    force_stopped: str = field_from_dict()
    skipped: str = field_from_dict()


@dataclass
class Group(DataclassFromDict):
    registration: Registration = field_from_dict()
    nothing_to_stop: str = field_from_dict()


@dataclass
class Localization(DataclassFromDict):
    Locale: str = field_from_dict()
    language: str = field_from_dict()
    private: Private = field_from_dict()
    group: Group = field_from_dict()
