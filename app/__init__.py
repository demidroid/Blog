from sanic import Sanic

from .config import config
from app.models import tables


def create_app(config_name):
    app = Sanic('Blog')
    app.config.from_envvar(config[config_name])

