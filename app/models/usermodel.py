from .basemodel import BaseModel
from peewee import *
from app.utils.security import generate_password, verify_password


class User(BaseModel):
    email = CharField(unique=True)
    username = CharField()
    password = CharField(max_length=256)

    def verify(self, password):
        return verify_password(password, self.password)

    @classmethod
    async def get_by_email(cls):
        query = cls.select()
        result = await cls.pee.execute(query)
        if result:
            return result._result
        return
