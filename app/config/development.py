from .base import BaseConfig
from os import environ


class DevelopConfig(BaseConfig):
    DATABASE = {
        "database": environ.get('DATABASE'),
        "user": environ.get('USER'),
        "password": environ.get('PASSWORD'),
        "port": environ.get('PORT'),
        "host": environ.get('HOST'),
        "max_connections": 20
    }
