from aiohttp import web
from aiohttp.web_request import Request

ErrorsRoutes = web.RouteTableDef()


@ErrorsRoutes.get('/errors')
async def get_errors_handler(request: Request):
    pass


@ErrorsRoutes.get('/errors/{id}')
async def get_errors_handler(request: Request):
    pass
