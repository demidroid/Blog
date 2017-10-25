from sanic.response import json
from sanic import Blueprint

from app.base import BaseView
from app.models import User
from .schema import UserSchema, MyInfoSchema
from app.utils.http_response import Response
from app.decorators import login_require

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


user_bp.add_route(UserInfoView.as_view(), '/<pk:int>/info')
user_bp.add_route(MyInfoView.as_view(), '/my/info')
