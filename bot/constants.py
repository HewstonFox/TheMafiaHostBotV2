from config import env
import sys

IS_WEBHOOK = len(sys.argv) > 1
WEBHOOK_PATH = f'/webhook/{env.BOT_TOKEN}'
WEBHOOK_HOST = sys.argv[2] if len(sys.argv) > 2 else env.BASE_URI
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = sys.argv[1] if IS_WEBHOOK else env.PORT
