from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict

_ = field_from_dict


@dataclass
class PrivateButton(DataclassFromDict):
    more: str = _()


@dataclass
class GroupButton:
    connect: str = _()


@dataclass
class Private(DataclassFromDict):
    start: str = _()
    help: str = _()
    more_description: str = _()
    user_connected: str = _()
    user_left: str = _()
    button: PrivateButton = _()


@dataclass
class Registration(DataclassFromDict):
    start: str = _()
    already_started: str = _()
    reminder: str = _()
    force_stopped: str = _()
    skipped: str = _()
    reduced: str = _()
    extended: str = _()


@dataclass
class SettingsMenuProperty(DataclassFromDict):
    name: str = _()
    description: str = _()


@dataclass
class SettingsMenuCommandsOptions(DataclassFromDict):
    admin_only: str = _()
    all: str = _()


@dataclass
class SettingsMenuCommands(DataclassFromDict):
    name: str = _()
    description: str = _()
    game: str = _()
    start: str = _()
    stop: str = _()
    extend: str = _()
    reduce: str = _()
    options: SettingsMenuCommandsOptions = _()


@dataclass
class SettingsMenuTimeValues(DataclassFromDict):
    registration: SettingsMenuProperty = _()
    extend: SettingsMenuProperty = _()
    reduce: SettingsMenuProperty = _()
    night: SettingsMenuProperty = _()
    day: SettingsMenuProperty = _()
    poll: SettingsMenuProperty = _()
    vote: SettingsMenuProperty = _()


@dataclass
class SettingsMenuTime(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: SettingsMenuTimeValues = _()


@dataclass
class SettingsMenuPlayersValues(DataclassFromDict):
    max: SettingsMenuProperty = _()
    min: SettingsMenuProperty = _()


@dataclass
class SettingsMenuPlayers(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: SettingsMenuPlayersValues = _()


@dataclass
class SettingsMenuGameValues(DataclassFromDict):
    start_at_night: str = _()
    mute_messages_from_dead: str = _()
    show_role_of_dead: str = _()
    show_role_of_departed: str = _()
    show_killer: str = _()
    allow_mafia_chat: str = _()
    show_night_actions: str = _()
    show_private_night_actions: str = _()
    last_words: str = _()
    commissioner_can_kill: str = _()
    show_live_roles: str = _()
    show_message_on_vote: str = _()


@dataclass
class SettingsMenuGameOptions(DataclassFromDict):
    enable: str = _()
    disable: str = _()
    anonymously: str = _()
    without_numbers: str = _()


@dataclass
class SettingsMenuGame(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: SettingsMenuGameValues = _()
    options: SettingsMenuGameOptions = _()


@dataclass
class SettingsMenuRolesValues(DataclassFromDict):
    maf: SettingsMenuProperty = _()
    scd: SettingsMenuProperty = _()
    whr: SettingsMenuProperty = _()
    doc: SettingsMenuProperty = _()
    shr: SettingsMenuProperty = _()


@dataclass
class SettingsMenuRolesOptions(DataclassFromDict):
    enable: str = _()
    disable: str = _()


@dataclass
class SettingsMenuRoles(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: SettingsMenuRolesValues = _()
    options: SettingsMenuRolesOptions = _()


@dataclass
class SettingsMenuValues(DataclassFromDict):
    language: SettingsMenuProperty = _()
    command_rights: SettingsMenuCommands = _()
    time: SettingsMenuTime = _()
    players: SettingsMenuPlayers = _()
    game: SettingsMenuGame = _()
    roles: SettingsMenuRoles = _()


@dataclass
class SettingsMenu(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: SettingsMenuValues = _()


@dataclass
class Group(DataclassFromDict):
    registration: Registration = _()
    nothing_to_stop: str = _()
    nothing_to_reduce: str = _()
    nothing_to_extend: str = _()
    button: GroupButton = _()
    settings_menu: SettingsMenu = _()


@dataclass
class Session(DataclassFromDict):
    is_not_active: str = _()
    registration_already_ended: str = _()


@dataclass
class Player(DataclassFromDict):
    already_join: str = _()
    joined: str = _()


@dataclass
class CallbackQuery(DataclassFromDict):
    session: Session = _()
    player: Player = _()


@dataclass
class PrivateCommands(DataclassFromDict):
    start: str = _()
    help: str = _()


@dataclass
class GroupCommands(DataclassFromDict):
    start: str = _()
    help: str = _()
    game: str = _()
    reduce: str = _()
    extend: str = _()
    leave: str = _()
    settings: str = _()
    stop: str = _()


@dataclass
class Commands(DataclassFromDict):
    private: PrivateCommands = _()
    group: GroupCommands = _()


@dataclass
class Localization(DataclassFromDict):
    Locale: str = _()
    language: str = _()
    private: Private = _()
    group: Group = _()
    callback_query: CallbackQuery = _()
    commands: Commands = _()
