from sanic import Blueprint
from sanic.response import json

from app.base import BaseView, PageSchema
from app.decorators import login_require
from .schema import BlogSchema, BaseBlogSchema, BlogsSchema, BaseUserSchema, PatchBlogSchema
from app.models import Blog, User
from app.utils.http_response import Response

blog_bp = Blueprint('blog')


class BlogView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request):
        """
        @api {post} /blog 博客发布
        @apiVersion 0.0.1
        @apiName blog-create
        @apiDescription 发布博客
        @apiGroup Blog

        @apiParam {string} title blog标题
        @apiParam {string} content blog内容

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 49
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": {
                "content": "firstjob",
                "title": "lalalla"
            }

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

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 401 Unauthorized
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1001,
            "message": "账号或密码错误"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 120
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1002,
            "message": "请求参数有误",
            "result": {
                "content": [
                    "Missing data for required field."
                ]
            }
        }

        """
        current_user = request['current_user']
        self._check_request(request, BlogSchema)
        if self.error:
            return self.error_resp

        blog = await Blog.db_create(author=current_user, **self.request_arg)
        if not blog:
            return json(Response.make(code=1000), status=400)

        self._check_data(blog, BlogSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))


class BlogsView(BaseView):

    async def get(self, request):
        """
        @api {post} /blogs 博客查询
        @apiVersion 0.0.1
        @apiName Blogs-get
        @apiDescription 查询博客
        @apiGroup Blog

        @apiParam {String} [sort=create_time] 排序条件
        @apiParam {Integer} [page=1] 页码
        @apiParam {Integer} [count=10] 每页数量
        @apiParam {Integer=0,1} [desc=0] 是否倒序排列

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 253
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": [
                {
                    "author": {
                        "email": "1209518758@qq.com",
                        "id": 1,
                        "username": "yjgao"
                    },
                    "content": "firstjob",
                    "title": "lalalla"
                },
                {
                    "author": {
                        "email": "1209518758@qq.com",
                        "id": 1,
                        "username": "yjgao"
                    },
                    "content": "firstjob",
                    "title": "lalalla"
                }
            ]
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
        self._check_request(request, PageSchema)

        blogs = await Blog.get_by(**self.request_arg, is_delete=False)
        self._check_data(blogs, BlogsSchema(many=True))
        if self.error:
            return self.error_resp
        return json(Response.make(result=self.response_arg))


class UserBlogView(BaseView):

    async def get(self, request, pk):
        """
       @api {get} /<pk:int>/blogs 用户博客查询
       @apiVersion 0.0.1
       @apiName user-blogs
       @apiDescription 查询用户博客
       @apiGroup User

       @apiParam {String} [sort=create_time] 排序条件
       @apiParam {Integer} [page=1] 页码
       @apiParam {Integer} [count=10] 每页数量
       @apiParam {Integer=0,1} [desc=0] 是否倒序排列

       @apiSuccessExample {json} Success-Response:
       HTTP/1.1 200 OK
       Connection: keep-alive
       Content-Length: 253
       Content-Type: application/json
       Keep-Alive: 60

       {
           "code": 0,
           "message": "success",
           "result": {
                 "author": {
                    "follow_value": 0,
                    "followed_value": 0,
                    "gender": 2,
                    "id": 1,
                    "username": "loyo"
                 },
                 "blogs": [
                     {
                        "content": "lallala",
                        "create_time": "11:27:59.981733+00:00",
                        "id": 1,
                        "like_value": 0,
                        "title": "llalalla"
                     }
                 ]
            }

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
        self._check_request(request, PageSchema)
        user = await User.db_get(id=pk)
        blogs = await Blog.get_by(**self.request_arg, author=user, is_delete=False)
        if not blogs:
            return json(Response.make(code=1002), status=400)
        self._check_data(blogs, BaseBlogSchema(many=True))
        if self.error:
            return self.error_resp

        result = {"blogs": self.response_arg}

        self._check_data(user, BaseUserSchema())
        if self.error:
            return self.error_resp
        result.update({"author": self.response_arg})

        return json(Response.make(result=result))


class MyBlogView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request):
        """
        @api {get} /my/blogs 我的博客
        @apiVersion 0.0.1
        @apiName my-blogs
        @apiDescription 获取我的博客
        @apiGroup Blog

        @apiParam {String} [sort=create_time] 排序条件
        @apiParam {Integer} [page=1] 页码
        @apiParam {Integer} [count=10] 每页数量
        @apiParam {Integer=0,1} [desc=0] 是否倒序排列

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 193
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": {
                "author": {
                    "follow_value": 0,
                    "followed_value": 0,
                    "gender": 2,
                    "id": 1,
                    "username": "loyo"
                },
                "blogs": [
                    {
                        "content": "lallala",
                        "create_time": "11:27:59.981733+00:00",
                        "id": 1,
                        "like_value": 0,
                        "title": "llalalla"
                    }
                ]
            }
        }


        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 120
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1000,
            "message": "系统错误"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 401 Unauthorized
        Connection: keep-alive
        Content-Length: 68
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1001,
            "message": "账号或密码错误"
        }
        """
        self._check_request(request, PageSchema)
        if self.error:
            return self.error_resp
        current_user = request.get('current_user')
        blogs = await Blog.get_by(**self.request_arg, author=current_user, is_delete=False)
        self._check_data(blogs, BaseBlogSchema(many=True))
        if self.error:
            return self.error_resp

        result = {"blogs": self.response_arg}

        self._check_data(current_user, BaseUserSchema())
        if self.error:
            return self.error_resp
        result.update({"author": self.response_arg})

        return json(Response.make(result=result))


class SingleBlogView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request, blog_id):
        """
        @api {get} /blogs/<blog_id:int> 查看单个博客内容
        @apiVersion 0.0.1
        @apiName Single-blog
        @apiDescription 查询单个博客的具体内容
        @apiGroup Blog

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 280
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": {
                "author": {
                    "follow_value": 0,
                    "followed_value": 0,
                    "gender": 2,
                    "id": 1,
                    "username": "jjjj"
                },
                "content": "yyyyyy",
                "create_time": "20:20:01.730670+00:00",
                "id": 1,
                "is_delete": false,
                "last_update_time": "20:20:01.730676+00:00",
                "like_value": 0,
                "title": "wwwww"
            }
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 120
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1000,
            "message": "系统错误"
        }
        """
        blog = await Blog.db_get(id=blog_id, is_delete=False)
        self._check_data(blog, BlogsSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))

    async def patch(self, request, blog_id):
        """
        @api {patch} /blogs/<blog_id:int> 修改博客数据
        @apiVersion 0.0.1
        @apiName update-blog
        @apiDescription 修改博客的数据
        @apiGroup Blog

        @apiParam {string} [title] 博客标题
        @apiParam {string} [content] 博客内容

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 280
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": {
                "author": {
                    "follow_value": 0,
                    "followed_value": 0,
                    "gender": 2,
                    "id": 1,
                    "username": "jjjj"
                },
                "content": "yyyyyy",
                "create_time": "20:20:01.730670+00:00",
                "id": 1,
                "is_delete": false,
                "last_update_time": "20:20:01.730676+00:00",
                "like_value": 0,
                "title": "wwwww"
            }
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 50
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1003,
            "message": "权限不足"
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
        current_user = request.get('current_user')
        self._check_request(request, PatchBlogSchema)
        if self.error:
            return self.error_resp

        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)

        if not current_user.id == blog.author_id:
            return json(Response.make(code=1003), status=400)

        blog_n = await blog.db_update(**self.request_arg)
        if not blog_n:
            return json(Response.make(code=1004), status=400)
        return await self.get(request, blog_id)

    async def delete(self, request, blog_id):
        """
        @api {delete} /blogs/<blog_id:int> 删除博客
        @apiVersion 0.0.1
        @apiName delete-blog
        @apiDescription 删除博客
        @apiGroup Blog

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 280
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success"
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 50
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1003,
            "message": "权限不足"
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
        current_user = request.get('current_user')
        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)

        if not current_user.id == blog.author_id:
            return json(Response.make(code=1003), status=400)

        blog_n = await blog.db_update(is_delete=True)
        if not blog_n:
            return json(Response.make(code=1004), status=400)
        return json(Response.make())


blog_bp.add_route(BlogView.as_view(), '/blog')
blog_bp.add_route(BlogsView.as_view(), '/blogs')
blog_bp.add_route(UserBlogView.as_view(), 'user/<pk:int>/blogs')
blog_bp.add_route(MyBlogView.as_view(), '/my/blogs')
blog_bp.add_route(SingleBlogView.as_view(), '/blogs/<blog_id:int>')
