from dataclasses import dataclass

from dict_to_dataclass import field_from_dict, DataclassFromDict


@dataclass
class LStrings(DataclassFromDict):
    somebody_of_them: str = field_from_dict()
    back: str = field_from_dict()
    close: str = field_from_dict()
