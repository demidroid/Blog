import logging
import peewee
from peewee_async import Manager

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

database = peewee.Proxy()


class BaseModel(peewee.Model):
    peewee.PostgresqlDatabase.interpolation = '%s'
    pee = Manager(database)
    data = list()
    error = (peewee.IntegrityError, peewee.InternalError, peewee.NotSupportedError)

    class Meta:
        database = database

    @classmethod
    async def db_get(cls, **kwargs):
        try:
            result = await cls.pee.get(cls, **kwargs)
        except peewee.DoesNotExist:
            result = None
        return result

    @classmethod
    async def db_create(cls, **kwargs):
        try:
            result = await cls.pee.create(cls, **kwargs)
        except cls.error:
            result = None
        return result

    async def db_update(self, **kwargs):
        try:
            for name, value in kwargs.items():
                setattr(self, name, value)
            result = await self.pee.update(self)
        except self.error:
            result = None
        return result

    @classmethod
    async def db_delete(cls, obj):
        try:
            result = await cls.pee.delete(obj)
        except cls.error:
            result = None
        return result

