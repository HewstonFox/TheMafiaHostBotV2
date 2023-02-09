from typing import Union, Type

from aiohttp.abc import AbstractView
from aiohttp.typedefs import Handler
from aiohttp.web_request import Request

from bot.routes.helpers.utils import check_auth


def with_auth(handler: Union[Type[AbstractView], Handler]):
    async def wrapper(request: Request):
        check_auth(request)
        return await handler(request)

    return wrapper
