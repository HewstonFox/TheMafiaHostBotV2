import io
import json
import operator
from functools import reduce

from aiogram.types import InputFile
from schema import SchemaError

from bot.controllers.SessionController.settings.presets import SettingsPreset
from bot.controllers.SessionController.settings.schema import settings_schema
from bot.localization import get_default_translation_index
from bot.utils.shared import dict_merge


class Settings:
    def __init__(self, *, lang: str = None, config: dict = None):
        if not config:
            self.values = dict_merge(SettingsPreset.default, {'language': lang or get_default_translation_index()})
            return

        if Settings.validate(config):
            self.values = config
            return

        raise SchemaError

    def apply_preset(self, preset: str):
        if not hasattr(SettingsPreset, preset):
            return SchemaError

        self.values = dict_merge(self.values, getattr(SettingsPreset, preset))

    def get_property(self, key: str):
        keys = key.split('.')
        if len(keys) == 1 and not keys[0]:
            return self.values
        return reduce(operator.getitem, key.split('.'), self.values)

    def set_property(self, key: str, value):
        try:
            key_list = key.split('.')
            path = self.get_property('.'.join(key_list[:-1]))
            prop = key_list[-1]
            if len(key_list) > 1 and key_list[-2] == 'players':
                if prop == 'min' and path['max'] < value:
                    return False
                if prop == 'max' and path['min'] > value:
                    return False
            path[prop] = value
            return True
        except KeyError:
            return False

    def export(self) -> io.IOBase:
        return io.BytesIO(json.dumps(self.values, indent=2).encode('utf-8'))

    def apply_from_file(self, file: io.IOBase):
        with file as f:
            try:
                values = json.load(f)
            except json.decoder.JSONDecodeError:
                raise SchemaError('Invalid json format')
            Settings.validate(values, True)
        self.values = values

    @classmethod
    def validate(cls, values: dict, strict: bool = False):
        try:
            settings_schema.validate(values)
            if values['players']['min'] > values['players']['max']:
                raise SchemaError('Key \'players\' error:\n'
                                  'Key \'min\' error:\n'
                                  'players.min can`t be more than players.max')
            return True
        except SchemaError as e:
            if strict:
                raise e
            return False
