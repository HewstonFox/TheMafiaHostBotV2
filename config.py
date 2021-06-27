import os

from dotenv import dotenv_values


class Environment:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


env_data = {**dotenv_values(".env"), **dotenv_values(".env.develop")}

env = Environment(**env_data, **os.environ)
