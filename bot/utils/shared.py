import asyncio
from itertools import islice
from asyncio import ALL_COMPLETED
from collections.abc import Mapping
from time import time
import copy
from typing import Awaitable, Callable, Any, Type

from aiohttp import ClientSession

from bot.constants import WEBHOOK_HOST


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


async def async_wait(fs, *, loop=None, timeout=None, return_when=ALL_COMPLETED):
    if not fs:
        return
    return await asyncio.wait(fs, loop=loop, timeout=timeout, return_when=return_when)


def count_bases_depth(class_type: Type) -> int:
    bases = class_type.__bases__
    if not len(bases):
        return 1
    return 1 + max([count_bases_depth(sub) for sub in bases])


def chunks(lst, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield islice(lst, i, i + n)


def flat_list(lst: Any) -> list:
    result = []
    if not isinstance(lst, list):
        return [lst]

    for item in list(lst):
        result.extend(flat_list(item))

    return result


async def ping_pong(timeout: int = 60):
    while True:
        async with ClientSession() as session:
            response = await session.get(f'{WEBHOOK_HOST}/ping')
            text = await response.text()
            if text != 'pong':
                print('Ping-Pong: WTF???', text)
            else:
                print('Ping-Pong: Success...')
        await asyncio.sleep(timeout)


def batch_str(value: str, size: int) -> list[str]:
    return [value[i:i + size] for i in range(0, len(value), size)]
