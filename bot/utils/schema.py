from schema import SchemaError


def field_range(_min: int = None, _max: int = None):
    def validator(value):
        if _min and value < _min:
            raise SchemaError(f'value {value} can`t be smaller than {_min}')
        if _max and value > _max:
            raise SchemaError(f'value {value} can`t be bigger than {_max}')
        return True

    return validator
