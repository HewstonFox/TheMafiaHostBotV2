import traceback
from datetime import datetime
from typing import Optional

from bot.controllers import DispatcherProvider
from bot.controllers.ErrorController.types import Error, ErrorContext


class ErrorController(DispatcherProvider):
    __errors: list[Error] = []

    @classmethod
    def add_error(cls, error: Exception, context: Optional[ErrorContext] = None) -> Error:
        record: Error = {
            'id': round(datetime.now().timestamp()),
            'error': repr(error),
            'trace': traceback.format_exception(type(error), error, error.__traceback__),
            'context': context if context else {}
        }
        cls.__errors.append(record)
        return record

    @classmethod
    def get_errors(cls) -> list[Error]:
        return cls.__errors

    @classmethod
    def get_error(cls, error_id: int) -> Optional[Error]:
        return next((x for x in cls.__errors if x['id'] == error_id), None)

    @classmethod
    def remove_error(cls, error_id: int) -> Optional[Error]:
        record = cls.get_error(error_id)
        if record is None:
            return None
        cls.__errors.remove(record)
        return record
