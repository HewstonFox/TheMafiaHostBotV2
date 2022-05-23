from dataclasses import dataclass
from dict_to_dataclass import DataclassFromDict, field_from_dict


@dataclass
class LAuthOptions(DataclassFromDict):
    confirm: str = field_from_dict()
    reject: str = field_from_dict()


@dataclass
class LAuth(DataclassFromDict):
    request: str = field_from_dict()
    success: str = field_from_dict()
    reject: str = field_from_dict()
    failure: str = field_from_dict()
    options: LAuthOptions = field_from_dict()
