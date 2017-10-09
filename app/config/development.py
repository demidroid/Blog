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

    REDIS = {
        "address": ('localhost', 6379),
        "minsize": 5,
        "maxsize": 10
    }

    EMAIL = {
        "from_addr": "example@163.com",
        "password": "Y7B9XA5EsdaddDda",
        "smtp_server": "smtp.163.com"
    }
