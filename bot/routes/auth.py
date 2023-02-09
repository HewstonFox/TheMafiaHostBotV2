from aiohttp import web
from aiohttp.web_request import Request

from bot.constants import WEBHOOK_HOST
from bot.controllers.AuthController.AuthController import AuthController
from bot.controllers.UserController.collection import find_user_record
from bot.controllers.UserController.types import UserRecord
from config import env

AuthRoutes = web.RouteTableDef()


@AuthRoutes.post('/login/{user}')
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


@AuthRoutes.post('/logout')
async def logout_handler(request: Request):
    res = web.Response(status=200, text='Success')
    res.del_cookie(env.COOKIE_KEY)
    return res
