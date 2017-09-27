from .base import BaseConfig


class TestConfig(BaseConfig):
    DATABASE = {
        "database": 'blog',
        "user": 'yjgao',
        "password": '123456',
        "port": 5432,
        "host": "127.0.0.1",
        "max_connections": 20
    }

    REDIS = {
        "address": ('localhost', 6379),
        "minsize": 5,
        "maxsize": 10
    }

    EMAIL = {
        "from_addr": "15757164314@163.com",
        "password": "Y7B9XA5EqsrA9YRU",
        "smtp_server": "smtp.163.com"
    }
