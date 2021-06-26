import os
import json

dirname = os.path.dirname(__file__)
locales_files = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f)) and f.endswith('.json')]


class Localization:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


translations = {}

for f in locales_files:
    with open(os.path.join(dirname, f), encoding='utf-8') as translation:
        translations[f.split('.')[0]] = Localization(**json.load(translation))


def t(locale: str):
    return translations['en' if locale not in translations else locale]
