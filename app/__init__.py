from sanic import Sanic
from peewee_async import PooledPostgresqlDatabase, Manager

from .config import config
from .models import database
from .models.basemodel import BaseModel

from .auth import auth_bp
from .home import home_bp


def create_app(config_name):
    app = Sanic('Blog')
    app.config.from_envvar(config[config_name])

    app.blueprint(auth_bp)
    app.blueprint(home_bp)

    @app.listener('before_server_start')
    async def set_db(_app, _loop):
        database.initialize(PooledPostgresqlDatabase(**app.config.DATABASE))
        BaseModel.pee = Manager(database, loop=_loop)

    return app
