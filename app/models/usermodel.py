from .basemodel import BaseModel
from peewee import *
from app.utils.security import generate_password


class User(BaseModel):
    email = CharField(unique=True)
    username = CharField()
    password = CharField(max_length=256)
    active = BooleanField(default=False)

    async def gen_confirm_code(self, request, token):
        code_dict = {
            "key": token,
            "id": self.id
        }
        with await request.app.redis as coon:
            tr = coon.multi_exec()
            tr.hmset_dict(token, code_dict)
            tr.expire(token, request.app.config.TOKEN_EXPIRE)
            await tr.execute()
        return token
