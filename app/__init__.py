import aioredis
from sanic import Sanic
from peewee_async import PooledPostgresqlDatabase, Manager
from sanic.response import json

from .config import config
from .models import database
from .models.basemodel import BaseModel
from app.models import User
from app.utils.http_response import Response


from .auth import auth_bp


def create_app(config_name):
    app = Sanic('Blog')
    app.config.from_object(config[config_name])

    app.blueprint(auth_bp)

    @app.listener('before_server_start')
    async def set_db(_app, _loop):
        database.initialize(PooledPostgresqlDatabase(**app.config.DATABASE))
        BaseModel.pee = Manager(database, loop=_loop)
        app.redis = await aioredis.create_pool(**app.config.REDIS)

    @app.middleware('request')
    async def auth_require(request):
        authorization = request.headers.get('authorization')
        if authorization:
            _, token = authorization.split(" ")
            if _.upper() == 'TOKEN':
                with await request.app.redis as coon:
                    redis_token, user_id = await coon.hmget(token, 'key', 'id')
                    if redis_token:
                        if redis_token.decode() == token:
                            request['current_user'] = await User.db_get(id=user_id.decode())
                        else:
                            return json(Response.make(code=1001), status=401)

    return app
