from time import time
import collections


def get_current_time() -> int:
    return int(time() * 1000)


def is_error(value):
    return issubclass(type(value), Exception)


def raise_if_error(value):
    if is_error(value):
        raise value


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
