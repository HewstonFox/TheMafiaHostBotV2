from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class PrivateButton(DataclassFromDict):
    more: str = field_from_dict()


@dataclass
class GroupButton:
    connect: str = field_from_dict()


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
    reduced: str = field_from_dict()
    extended: str = field_from_dict()


@dataclass
class Group(DataclassFromDict):
    registration: Registration = field_from_dict()
    nothing_to_stop: str = field_from_dict()
    nothing_to_reduce: str = field_from_dict()
    nothing_to_extend: str = field_from_dict()
    button: GroupButton = field_from_dict()


@dataclass
class Session(DataclassFromDict):
    is_not_active: str = field_from_dict()
    registration_already_ended: str = field_from_dict()


@dataclass
class Player(DataclassFromDict):
    already_join: str = field_from_dict()
    joined: str = field_from_dict()


@dataclass
class CallbackQuery(DataclassFromDict):
    session: Session = field_from_dict()
    player: Player = field_from_dict()


@dataclass
class PrivateCommands(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()


@dataclass
class GroupCommands(DataclassFromDict):
    start: str = field_from_dict()
    help: str = field_from_dict()
    game: str = field_from_dict()
    reduce: str = field_from_dict()
    extend: str = field_from_dict()
    leave: str = field_from_dict()
    settings: str = field_from_dict()
    stop: str = field_from_dict()


@dataclass
class Commands(DataclassFromDict):
    private: PrivateCommands = field_from_dict()
    group: GroupCommands = field_from_dict()


@dataclass
class Localization(DataclassFromDict):
    Locale: str = field_from_dict()
    language: str = field_from_dict()
    private: Private = field_from_dict()
    group: Group = field_from_dict()
    callback_query: CallbackQuery = field_from_dict()
    commands: Commands = field_from_dict()
