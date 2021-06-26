from bot import start_bot
from config import env

if __name__ == '__main__':
    print(f'Starting in {env.MODE} mode.')
    start_bot()
