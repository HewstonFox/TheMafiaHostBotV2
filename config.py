import os

from dotenv import dotenv_values


class Environment:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return ''


env_data = {**dotenv_values(".env"), **dotenv_values(".env.develop")}

env = Environment(**env_data, **os.environ)
