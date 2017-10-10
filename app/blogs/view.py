from sanic import Blueprint
from sanic.response import json

from app.base import BaseView
from app.decorators import login_require
from .schema import BlogSchema
from app.models import Blog
from app.utils.http_response import Response

blog_bp = Blueprint('blog')


class BlogView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request):
        current_user = request['current_user']
        self._check_request(request, BlogSchema)
        if self.error:
            return self.error_resp

        blog = await Blog.db_create(user=current_user, **self.request_arg)
        if not blog:
            return json(Response.make(code=1000), status=400)

        self._check_data(blog, Blog)
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))

blog_bp.add_route(BlogView.as_view(), '/blog')
