import asyncpg
from peewee import *
from peewee import Database

from app.utils.sql import pg_sql


class BaseModel(Model):
    Database.interpolation = '%s'
    create_sql = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_sql.append(self.sqlall())
        self.create_table()
