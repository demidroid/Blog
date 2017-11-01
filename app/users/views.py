from sanic.response import json
from sanic import Blueprint

from app.base import BaseView
from app.models import User, Follow
from .schema import UserSchema, MyInfoSchema, FollowedSchema, FollowerSchema
from app.utils.http_response import Response
from app.decorators import login_require
from app.base.schema import PageSchema

user_bp = Blueprint('user')


class UserInfoView(BaseView):

    async def get(self, request, pk):
        """
        @api {get} /<pk:int>/info 用户信息
        @apiVersion 0.0.1
        @apiName user-info
        @apiDescription 获取某一用户的信息
        @apiGroup User

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
                "create_time": "09:22:56.251781+00:00",
                "follow_value": 0,
                "followed_value": 0,
                "gender": 2,
                "id": 1,
                "last_login_time": "09:22:56.251787+00:00",
                "username": "loyo"
            }
        }

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
        users = await User.db_get(id=pk)
        self._check_data(users, UserSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))


class MyInfoView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request):
        """
        @api {get} /my/info 获取我的信息
        @apiVersion 0.0.1
        @apiName my-info
        @apiDescription 获取我的个人信息
        @apiGroup My

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
                "create_time": "09:22:56.251781+00:00",
                "email": "1209518758@qq.com",
                "follow_value": 0,
                "followed_value": 0,
                "gender": 2,
                "id": 1,
                "last_login_time": "09:22:56.251787+00:00",
                "username": "loyo"
            }
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
        current_user = request.get('current_user')
        user = await User.db_get(id=current_user.id)
        self._check_data(user, MyInfoSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))

    async def patch(self, request):
        """
        @api {patch} /my/info 修改我的信息
        @apiVersion 0.0.1
        @apiName my-info-patch
        @apiDescription 对个人信息修改
        @apiGroup My

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
                "create_time": "09:22:56.251781+00:00",
                "follow_value": 0,
                "followed_value": 0,
                "gender": 2,
                "id": 1,
                "last_login_time": "09:22:56.251787+00:00",
                "username": "loyo"
            }
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
        current_user = request.get('current_user')
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        current_user = await current_user.db_update(**self.request_arg)
        if not current_user:
            return json(Response.make(code=1004), status=400)
        return await self.get(request)

    async def post(self, request):
        current_user = request.get('current_user')
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        current_user = await current_user.db_update(active=False)
        if not current_user:
            return json(Response.make(code=1004), status=400)
        return await self.get(request)


class FollowView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request, pk):
        """
        @api {post} /follow/<pk:int> 用户关注
        @apiVersion 0.0.1
        @apiName Follow
        @apiDescription 关注某个用户
        @apiGroup User

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
        current_user = request.get('current_user')
        follow_user = await User.db_get(id=pk)
        follow_record = await Follow.db_get(follower_id=current_user.id, followed_id=follow_user.id)
        if not follow_user:
            return json(Response.make(code=1005), status=400)
        result = await current_user.follow(follow_record=follow_record,
                                           follow_user=follow_user, current_user=current_user)
        if not result:
            return json(Response.make(code=1000), status=400)
        return json(Response.make(result='success'), status=200)


class GetFollowView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request):
        """
        @api {post} /my/follow 我关注的用户
        @apiVersion 0.0.1
        @apiName My-Follow
        @apiDescription 我关注的用户
        @apiGroup My

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 128
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": [
                {
                    "followed": {
                        "follow_value": 1,
                        "followed_value": 0,
                        "gender": 2,
                        "id": 1,
                        "username": "jjjj"
                    }
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
        follow_users = await Follow.get_by(**self.request_arg, follower=current_user)
        self._check_data(follow_users, FollowedSchema(many=True))
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))


class GetFollowedView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request):
        """
        @api {post} /my/follow 关注我的用户
        @apiVersion 0.0.1
        @apiName Follow－Me
        @apiDescription 关注的我用户
        @apiGroup My

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 128
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": [
                {
                    "follower": {
                        "follow_value": 1,
                        "followed_value": 0,
                        "gender": 2,
                        "id": 1,
                        "username": "jjjj"
                    }
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
        followed_users = await Follow.get_by(**self.request_arg, followed=current_user)
        self._check_data(followed_users, FollowerSchema(many=True))
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))

user_bp.add_route(UserInfoView.as_view(), 'users/<pk:int>/info')
user_bp.add_route(MyInfoView.as_view(), '/my/info')
user_bp.add_route(FollowView.as_view(), '/users/<pk:int>/follow')
user_bp.add_route(GetFollowView.as_view(), '/my/follow')
user_bp.add_route(GetFollowedView.as_view(), '/my/followed')
