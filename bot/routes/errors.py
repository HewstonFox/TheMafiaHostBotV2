import json

from aiohttp import web
from aiohttp.web_request import Request

from bot.controllers.ErrorController.ErrorController import ErrorController
from bot.routes.helpers.decorators import with_auth

ErrorsRoutes = web.RouteTableDef()


@ErrorsRoutes.get('/errors')
@with_auth
async def get_errors_handler(request: Request):
    return web.Response(body=json.dumps(ErrorController.get_errors()), content_type='application/json;utf-8')


@ErrorsRoutes.get('/errors/{id}')
@with_auth
async def get_error_handler(request: Request):
    error_id = request.match_info['id']
    try:
        error = ErrorController.get_error(int(error_id))
    except ValueError:
        raise web.HTTPBadRequest()
    if error is None:
        raise web.HTTPNotFound()
    return web.Response(
        body=json.dumps(error),
        content_type='application/json;utf-8'
    )


@ErrorsRoutes.delete('/errors/{id}')
@with_auth
async def delete_error_handler(request: Request):
    error_id = request.match_info['id']
    try:
        error = ErrorController.remove_error(int(error_id))
    except ValueError:
        raise web.HTTPBadRequest()
    if error is None:
        raise web.HTTPNotFound()
    return web.Response(
        body=json.dumps(error),
        content_type='application/json;utf-8'
    )
