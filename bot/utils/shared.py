from time import time


def get_current_time() -> int:
    return int(time() * 1000)
