import asyncio
from collections.abc import Mapping
from time import time
import copy
from typing import Awaitable, Callable, Any, Type


def get_current_time() -> int:
    return int(time() * 1000)


def is_error(value):
    return issubclass(type(value), Exception)


def raise_if_error(value):
    if is_error(value):
        raise value


def dict_merge(*dicts: dict):
    args_len = len(dicts)

    if args_len == 0:
        return {}

    target = copy.deepcopy(dicts[0])

    if args_len == 1:
        return target

    merge_dct = dicts[1]

    for k, v in merge_dct.items():
        if (k in target and isinstance(target[k], dict)
                and isinstance(merge_dct[k], Mapping)):
            target[k] = dict_merge(target[k], merge_dct[k])
        else:
            target[k] = merge_dct[k]

    return target if args_len < 3 else dict_merge(target, *dicts[2:])


async def async_timeout(timeout: int, func: Callable[[...], Awaitable[None]], *args, **kwargs):
    await asyncio.sleep(timeout)
    await func(*args, **kwargs)


def count_bases_depth(class_type: Type) -> int:
    bases = class_type.__bases__
    if not len(bases):
        return 1
    return 1 + max([count_bases_depth(sub) for sub in bases])
