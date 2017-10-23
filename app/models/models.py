import peewee
import datetime
from peewee import *
from .basemodel import BaseModel
from app.utils.security import generate_password, verify_password


class User(BaseModel):
    email = CharField(unique=True)
    username = CharField()
    password_hash = CharField(max_length=256)
    active = BooleanField(default=False)
    followed_value = SmallIntegerField(default=0)
    follow_value = SmallIntegerField(default=0)
    gender = SmallIntegerField(default=2)
    create_time = TimeField(default=datetime.datetime.now)
    last_login_time = TimeField(default=datetime.datetime.now)

    @property
    def password(self):
        return ValueError('NOT able To read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password(password)

    def verify_password(self, password):
        return verify_password(password, self.password_hash)

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

    @classmethod
    async def db_get(cls, **kwargs):
        try:
            result = await cls.pee.get(cls, **kwargs)
        except peewee.DoesNotExist:
            result = None
        return result


class Follow(BaseModel):
    follower = ForeignKeyField(User, related_name='follow_user')
    followed = ForeignKeyField(User, related_name='followed_user')
    create_time = TimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            (('follower', 'followed'), True),
        )


class Blog(BaseModel):
    author = ForeignKeyField(User, related_name='user')
    title = CharField(max_length=125)
    content = CharField(null=False)
    like_value = IntegerField(default=0)
    is_delete = BooleanField(default=False)
    create_time = TimeField(default=datetime.datetime.now)
    last_update_time = TimeField(default=datetime.datetime.now)

    @classmethod
    async def get_by(cls, count: int=10, page: int=1, sort: str='create_time', desc: int=0, **kwargs):
        try:
            order = getattr(cls, sort, 'create_time')
            if desc:
                order = order.desc()
            if kwargs:
                if kwargs.get("author"):
                    condition = getattr(cls, 'author_id')
                else:
                    condition = getattr(cls, list(kwargs.keys())[0])
                sql = cls.select().where().order_by(order).paginate(page, count)
            else:
                sql = cls.select().where().order_by(order).paginate(page, count)
            result = await cls.pee.execute(sql)
        except peewee.DoesNotExist:
            result = None
        return result


class Comment(BaseModel):
    author = ForeignKeyField(User, related_name='comment_user')
    blog_user = ForeignKeyField(User, related_name='blog_author')
    blog = ForeignKeyField(Blog, related_name='blog')
    content = CharField(null=False)
    like_value = IntegerField(default=0)
    is_delete = BooleanField(default=False)
    create_time = TimeField(datetime.datetime.now)

    @classmethod
    async def get_by(cls, count: int=10, page: int=1, sort: str='create_time', desc: int=0, **kwargs):
        try:
            order = getattr(cls, sort, 'create_time')
            if desc:
                order = order.desc()
            if kwargs:
                if kwargs.get("blog"):
                    condition = getattr(cls, 'blog.id')
                else:
                    condition = getattr(cls, list(kwargs.keys())[0])
                sql = cls.select().where(condition).order_by(order).paginate(page, count)
            else:
                sql = cls.select().where().order_by(order).paginate(page, count)
            result = await cls.pee.execute(sql)
        except peewee.DoesNotExist:
            result = None
        return result
