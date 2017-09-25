import codecs
import markdown
from sanic.response import file
from sanic import Blueprint
from app.base import BaseView

home_bp = Blueprint('home')


class HomeView(BaseView):

    async def get(self, request):
        return await file('./Home.html')

home_bp.add_route(HomeView.as_view(), '/')
