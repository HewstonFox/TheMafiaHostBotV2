from mimetypes import guess_type
from pathlib import Path

from aiohttp import web
from aiohttp.web_request import Request

from bot.routes.helpers.utils import check_auth

AppRoutes = web.RouteTableDef()


@AppRoutes.get('/')
async def index(request: Request):
    raise web.HTTPFound('/app')


@AppRoutes.get('/ping')
async def ping_handler(request: Request):
    return web.Response(text='pong')


@AppRoutes.get('/app')
@AppRoutes.get('/app/{tail:.*}')
async def app(request: Request):
    try:
        req_path_str = request.match_info['tail']
    except KeyError:
        req_path_str = ''

    if str(req_path_str).startswith('private'):
        check_auth(request, True)

    req_path = Path('app', req_path_str or 'index.html')
    req_path = req_path if req_path.suffix != '' else req_path.with_suffix('.html')
    req_path = req_path if req_path.exists() else Path('app', '404.html')

    with req_path.open('rb') as f:
        content = f.read()
    return web.Response(body=content, content_type=';'.join(filter(lambda x: x, guess_type(str(req_path)))))
