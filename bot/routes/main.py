from mimetypes import guess_type
from pathlib import Path

from aiohttp import web
from aiohttp.web_request import Request

from bot.constants import WEBHOOK_HOST
from bot.controllers.AuthController.AuthController import AuthController
from bot.controllers.UserController.collection import find_user_record
from bot.controllers.UserController.types import UserRecord
from config import env

MainRoutes = web.RouteTableDef()


def unauthorizedRedirect():
    res = web.HTTPSeeOther('/app/login')
    res.del_cookie(env.COOKIE_KEY)
    return res


@MainRoutes.get('/app')
@MainRoutes.get('/app/{tail:.*}')
async def app(request: Request):
    try:
        req_path_str = request.match_info['tail']
    except KeyError:
        req_path_str = ''

    if str(req_path_str).startswith('private'):
        if not AuthController.verify(request.cookies.get(env.COOKIE_KEY)):
            raise unauthorizedRedirect()

    req_path = Path('app', req_path_str or 'index.html')
    req_path = req_path if req_path.suffix != '' else req_path.with_suffix('.html')
    req_path = req_path if req_path.exists() else Path('app', '404.html')

    with req_path.open('rb') as f:
        content = f.read()
    return web.Response(body=content, content_type=';'.join(filter(lambda x: x, guess_type(str(req_path)))))


@MainRoutes.post('/login/{user}')
async def login_handler(request: Request):
    user: UserRecord = await find_user_record(request.match_info['user'])
    if not user or not user.get('is_admin'):
        raise web.HTTPUnauthorized()

    token = await AuthController.auth(user['chat_id'], WEBHOOK_HOST)
    if not token:
        raise web.HTTPUnauthorized()

    res = web.Response(status=200, text='Success')
    res.set_cookie(env.COOKIE_KEY, token, secure=True)

    return res


@MainRoutes.get('/{tail:.*}')
async def index(request: Request):
    raise web.HTTPFound('/app')
