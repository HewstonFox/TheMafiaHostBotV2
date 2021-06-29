import os
import json

from bot.localization.Localization import Localization

__translations: dict[str, Localization] = {}


def parse_localizations():
    dirname = os.path.join(os.path.dirname(__file__), 'translations')
    locales_files = [f for f in os.listdir(dirname) if
                     os.path.isfile(os.path.join(dirname, f)) and f.endswith('.json')]
    for f in locales_files:
        with open(os.path.join(dirname, f), encoding='utf-8') as translation:
            locale_name = f.split('.')[0]
            data: dict = json.load(translation)
            data['Locale'] = locale_name
            __translations[locale_name] = Localization.from_dict(data)


parse_localizations()


def get_translation(locale: str):
    return __translations['en' if locale not in __translations else locale]
