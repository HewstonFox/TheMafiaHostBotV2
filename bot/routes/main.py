from os import path

from aiohttp import web

MainRoutes = web.RouteTableDef()


@MainRoutes.get('/')
async def hello(request):
    with open(path.join('assets', 'pages', 'welcome_page.html'), encoding='utf-8') as f:
        content = f.read()
    return web.Response(text=content, content_type='text/html')
