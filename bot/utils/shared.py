from time import time


def get_current_time() -> int:
    return int(time() * 1000)


def is_error(value):
    return issubclass(type(value), Exception)


def raise_if_error(value):
    if is_error(value):
        raise value
