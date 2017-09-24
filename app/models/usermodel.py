from peewee import IntegerField, CharField
from .basemodel import BaseModel


class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField()
    password = CharField()

    @classmethod
    def user_id(cls):
        query = cls.select().where(cls.id == 1).sql()
        str_query = pg_sql(*query)
        print(str_query)