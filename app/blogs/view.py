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
        """
        @api {post} /follow/<pk:int> Follow
        @apiVersion 0.0.1
        @apiName Follow-user
        @apiDescription
        @apiGroup Auth

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 49
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": "Success"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 62
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1000,
            "message": "系统错误"
        }
        """
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
