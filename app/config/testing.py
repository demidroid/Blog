from .base import BaseConfig


class TestConfig(BaseConfig):
    DATABASE = {
        "database": 'blog',
        "user": 'yjgao',
        "password": '123456',
        "port": 5432,
        "host": "ec2-184-72-230-93.compute-1.amazonaws.com",
        "max_connections": 20
    }