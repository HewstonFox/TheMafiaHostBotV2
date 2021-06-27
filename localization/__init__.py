import os
import json
from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict

dirname = os.path.dirname(__file__)
locales_files = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f)) and f.endswith('.json')]


@dataclass
class PrivateButton(DataclassFromDict):
    more: str = field_from_dict()


@dataclass
class Private(DataclassFromDict):
    start: str = field_from_dict()
    button: PrivateButton = field_from_dict()


@dataclass
class Localization(DataclassFromDict):
    language: str = field_from_dict()
    private: Private = field_from_dict()


translations = {}

for f in locales_files:
    with open(os.path.join(dirname, f), encoding='utf-8') as translation:
        locale_name = f.split('.')[0]
        data = json.load(translation)
        translations[locale_name] = Localization.from_dict(data)


def get_translation(locale: str):
    return translations['en' if locale not in translations else locale]
