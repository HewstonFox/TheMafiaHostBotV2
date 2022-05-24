from aiohttp import web

from bot.controllers.AuthController.AuthController import AuthController
from config import env
from aiohttp.web_request import Request


def unauthorized_exception(redirect: bool = False):
    res = web.HTTPSeeOther('/app/login') if redirect else web.HTTPUnauthorized()
    res.del_cookie(env.COOKIE_KEY)
    return res


def check_auth(request: Request, redirect: bool = False):
    if not AuthController.verify(request.cookies.get(env.COOKIE_KEY)):
        raise unauthorized_exception(redirect)
