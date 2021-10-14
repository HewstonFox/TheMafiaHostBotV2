from dataclasses import dataclass

from dict_to_dataclass import field_from_dict, DataclassFromDict

_ = field_from_dict


@dataclass
class LGroupButton(DataclassFromDict):
    connect: str = field_from_dict()


@dataclass
class LSettingsMenuProperty(DataclassFromDict):
    name: str = field_from_dict()
    description: str = field_from_dict()


@dataclass
class LSettingsMenuTimeValues(DataclassFromDict):
    registration: LSettingsMenuProperty = _()
    extend: LSettingsMenuProperty = _()
    reduce: LSettingsMenuProperty = _()
    night: LSettingsMenuProperty = _()
    day: LSettingsMenuProperty = _()
    poll: LSettingsMenuProperty = _()
    vote: LSettingsMenuProperty = _()


@dataclass
class LSettingsMenuTime(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: LSettingsMenuTimeValues = _()


@dataclass
class LSettingsMenuPlayersValues(DataclassFromDict):
    max: LSettingsMenuProperty = _()
    min: LSettingsMenuProperty = _()


@dataclass
class LSettingsMenuPlayers(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: LSettingsMenuPlayersValues = _()


@dataclass
class LSettingsMenuRolesValues(DataclassFromDict):
    maf: LSettingsMenuProperty = _()
    scd: LSettingsMenuProperty = _()
    whr: LSettingsMenuProperty = _()
    doc: LSettingsMenuProperty = _()
    srg: LSettingsMenuProperty = _()
    lwr: LSettingsMenuProperty = _()
    lck: LSettingsMenuProperty = _()
    mnc: LSettingsMenuProperty = _()
    bum: LSettingsMenuProperty = _()


@dataclass
class LSettingsMenuRolesOptions(DataclassFromDict):
    enable: str = _()
    disable: str = _()


@dataclass
class LSettingsMenuRoles(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: LSettingsMenuRolesValues = _()
    options: LSettingsMenuRolesOptions = _()


@dataclass
class LSettingsMenuGameValues(DataclassFromDict):
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
    lynching_confirmation: str = _()
    show_live_roles: str = _()
    show_message_on_vote: str = _()


@dataclass
class LSettingsMenuGameOptions(DataclassFromDict):
    enable: str = _()
    disable: str = _()
    anonymously: str = _()
    without_numbers: str = _()


@dataclass
class LSettingsMenuCommandsOptions(DataclassFromDict):
    admin_only: str = _()
    all: str = _()


@dataclass
class LSettingsMenuCommands(DataclassFromDict):
    name: str = _()
    description: str = _()
    game: str = _()
    start: str = _()
    stop: str = _()
    extend: str = _()
    reduce: str = _()
    options: LSettingsMenuCommandsOptions = _()


@dataclass
class LSettingsMenuGame(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: LSettingsMenuGameValues = _()
    options: LSettingsMenuGameOptions = _()


@dataclass
class LSettingsMenuValues(DataclassFromDict):
    language: LSettingsMenuProperty = _()
    command_rights: LSettingsMenuCommands = _()
    time: LSettingsMenuTime = _()
    players: LSettingsMenuPlayers = _()
    game: LSettingsMenuGame = _()
    roles: LSettingsMenuRoles = _()


@dataclass
class LSettingsMenu(DataclassFromDict):
    name: str = _()
    description: str = _()
    values: LSettingsMenuValues = _()


@dataclass
class LRegistration(DataclassFromDict):
    start: str = _()
    already_started: str = _()
    nothing_to_skip: str = _()
    reminder: str = _()
    force_stopped: str = _()
    skipped: str = _()
    reduced: str = _()
    extended: str = _()


@dataclass
class LGame(DataclassFromDict):  #
    already_started: str = _()
    force_stopped: str = _()
    settings_unavailable: str = _()
    day_good: str = _()
    day_bad: str = _()
    night: str = _()
    voting: str = _()
    player_left_game: str = _()
    player_left_game_extended: str = _()
    vote_actor_chose_victim: str = _()
    no_candidate: str = _()
    too_much_candidates: str = _()
    endgame: str = _()


@dataclass
class LGroup(DataclassFromDict):
    registration: LRegistration = _()
    game: LGame = _()
    nothing_to_stop: str = _()
    nothing_to_reduce: str = _()
    nothing_to_extend: str = _()
    preset_applied: str = _()
    settings_apply_success: str = _()
    settings_apply_failure: str = _()
    button: LGroupButton = _()
    settings_menu: LSettingsMenu = _()
