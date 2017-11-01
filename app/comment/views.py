from sanic.response import json
from sanic import Blueprint

from app.base import BaseView, PageSchema
from app.utils.http_response import Response
from app.models import Comment, Blog
from .schema import CommentSchema
from app.decorators import login_require


comment_bp = Blueprint('comment')


class CommentsView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request, blog_id):
        """
        @api {get} /blogs/<blog_id:int>/comments 查询博客评论
        @apiVersion 0.0.1
        @apiName Blog-comments
        @apiDescription 查询一个博客的评论
        @apiGroup Comment

        @apiParam {String} [sort=create_time] 排序条件
        @apiParam {Integer} [page=1] 页码
        @apiParam {Integer} [count=10] 每页数量
        @apiParam {Integer=0,1} [desc=0] 是否倒序排列

        @apiSuccessExample {json} Success-response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 233
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": [
                {
                    "author": {
                        "follow_value": 0,
                        "followed_value": 0,
                        "gender": 2,
                        "id": 1,
                        "username": "jjjj"
                    },
                    "blog": 1,
                    "content": "yyyyyuu",
                    "create_time": "20:20:11.777450+00:00",
                    "id": 1,
                    "is_delete": false,
                    "like_value": 0
                }
            ]
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1005,
            "message": "请求资源不存在"
        }
        """
        self._check_request(request, PageSchema)
        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)

        comments = await Comment.get_by(**self.request_arg, blog=blog)

        self._check_data(comments, CommentSchema(many=True))
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))

    async def post(self, request, blog_id):
        """
        @api {post} /blogs/<blog_id:int>/comments 博客评论
        @apiVersion 0.0.1
        @apiName Post-comment
        @apiDescription 评论一个博客的评论
        @apiGroup Comment

        @apiSuccessExample {json} Success-response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 233
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": [
                {
                    "author": {
                        "follow_value": 0,
                        "followed_value": 0,
                        "gender": 2,
                        "id": 1,
                        "username": "jjjj"
                    },
                    "blog": 1,
                    "content": "yyyyyuu",
                    "create_time": "20:20:11.777450+00:00",
                    "id": 1,
                    "is_delete": false,
                    "like_value": 0
                }
            ]
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1005,
            "message": "请求资源不存在"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1004,
            "message": "数据库错误"
        }
        """
        self._check_request(request, CommentSchema)
        if self.error:
            return self.error_resp

        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)
        author = request.get('current_user')

        comment = await Comment.db_create(blog=blog, author=author, **self.request_arg)
        if not comment:
            return json(Response.make(code=1004), status=400)

        return await self.get(request, blog_id)


class CommentView(BaseView):
    decorators = [login_require('login')]

    async def delete(self, request, comment_id):
        """
        @api {delete} /blogs/<blog_id:int>/comments 删除博客评论
        @apiVersion 0.0.1
        @apiName Delete-Blog-comment
        @apiDescription 删除一个博客的评论一个评论
        @apiGroup Comment

        @apiSuccessExample {json} Success-response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 233
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1005,
            "message": "请求资源不存在"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1003,
            "message": "数据库错误"
        }
        """
        comment = await Comment.db_get(id=comment_id, is_delete=False)
        if not comment:
            return json(Response.make(code=1005), status=400)

        if not comment.author == request.get('current_user'):
            return json(Response.make(code=1003), status=400)
        await comment.db_update(is_delete=True)
        return json(Response.make())

comment_bp.add_route(CommentsView.as_view(), "/blogs/<blog_id:int>/comments")
comment_bp.add_route(CommentView.as_view(), "/comments/<comment_id:int>")
