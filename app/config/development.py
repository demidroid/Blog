from .base import BaseConfig
from os import environ


class DevelopConfig(BaseConfig):
    DATABASE = {
        "database": environ.get('DATABASE'),
        "user": environ.get('USER'),
        "password": environ.get('PASSWORD'),
        "port": 5432,
        "host": "ec2-184-72-230-93.compute-1.amazonaws.com",
        "max_connections": 20
    }
