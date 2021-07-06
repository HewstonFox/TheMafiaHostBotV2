from schema import SchemaError

from bot.controllers.SessionController.settings.presets import SettingsPreset
from bot.controllers.SessionController.settings.schema import settings_schema
from bot.utils.shared import dict_merge


class Settings:
    def __init__(self, *, lang: str = None, config: dict = None):
        if not config:
            self.values = dict_merge(SettingsPreset.default, {'language': lang or 'en'})
            return

        if Settings.validate(config):
            self.values = config
            return

        raise SchemaError

    def apply_preset(self, preset: str):
        if not hasattr(SettingsPreset, preset):
            return SchemaError

        self.values = dict_merge(self.values, getattr(SettingsPreset, preset))

    @classmethod
    def validate(cls, values: dict):
        try:
            settings_schema.validate(values)
            return True
        except SchemaError:
            return False
