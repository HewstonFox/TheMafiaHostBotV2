import os
import json
from dataclasses import dataclass
from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class ERole(DataclassFromDict):
    bum: str = field_from_dict()
    civ: str = field_from_dict()
    com: str = field_from_dict()
    doc: str = field_from_dict()
    don: str = field_from_dict()
    lwr: str = field_from_dict()
    lck: str = field_from_dict()
    maf: str = field_from_dict()
    mnc: str = field_from_dict()
    srg: str = field_from_dict()
    scd: str = field_from_dict()
    whr: str = field_from_dict()


@dataclass
class EAction(DataclassFromDict):
    bom: str = field_from_dict()
    kill: str = field_from_dict()
    don: str = field_from_dict()
    maf: str = field_from_dict()
    mnc: str = field_from_dict()
    com_kill: str = field_from_dict()
    doc: str = field_from_dict()
    com: str = field_from_dict()
    lwr: str = field_from_dict()
    whr: str = field_from_dict()


@dataclass
class Emoji(DataclassFromDict):
    role: ERole = field_from_dict()
    action: EAction = field_from_dict()


with open(os.path.join(os.path.dirname(__file__), 'emoji.json'), encoding='utf-8') as f:
    emoji = Emoji.from_dict(json.load(f))
