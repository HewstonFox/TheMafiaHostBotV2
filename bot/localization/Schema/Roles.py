from dataclasses import dataclass

from dict_to_dataclass import field_from_dict, DataclassFromDict


@dataclass
class LRole(DataclassFromDict):
    name: str = field_from_dict()
    greeting: str = field_from_dict()
    effect: str = field_from_dict()
    global_effect: str = field_from_dict()
    affect: str = field_from_dict()


@dataclass
class LPromotion(DataclassFromDict):
    don: str = field_from_dict()
    com: str = field_from_dict()


@dataclass
class LBum(DataclassFromDict):
    actor_visited_target: str = field_from_dict()
    nothing_interesting: str = field_from_dict()
    was_together: str = field_from_dict()


@dataclass
class LCom(DataclassFromDict):
    check_result: str = field_from_dict()
    global_effect_kill: str = field_from_dict()


@dataclass
class LChore(DataclassFromDict):
    mafia_opinion_divided: str = field_from_dict()
    promotion: LPromotion = field_from_dict()
    bum: LBum = field_from_dict()
    com: LCom = field_from_dict()


@dataclass
class LRoles(DataclassFromDict):
    bum: LRole = field_from_dict()
    civ: LRole = field_from_dict()
    com: LRole = field_from_dict()
    doc: LRole = field_from_dict()
    don: LRole = field_from_dict()
    lwr: LRole = field_from_dict()
    lck: LRole = field_from_dict()
    maf: LRole = field_from_dict()
    mnc: LRole = field_from_dict()
    srg: LRole = field_from_dict()
    scd: LRole = field_from_dict()
    whr: LRole = field_from_dict()
    chore: LChore = field_from_dict()
