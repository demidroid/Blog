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