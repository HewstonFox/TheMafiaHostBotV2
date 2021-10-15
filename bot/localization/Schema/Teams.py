from dataclasses import dataclass
from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class LTeam(DataclassFromDict):
    name: str = field_from_dict()
    won: str = field_from_dict()


@dataclass
class LTeams(DataclassFromDict):
    maf: LTeam = field_from_dict()
    civ: LTeam = field_from_dict()
    mnc: LTeam = field_from_dict()
    scd: LTeam = field_from_dict()
    BOTH: LTeam = field_from_dict()
