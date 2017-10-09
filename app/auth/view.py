from sanic import Blueprint
from sanic.response import json

from app.models import User
from app.base import BaseView
from app.utils import Response
from .schema import UserSchema
from app.utils.security import get_random_str
from app.utils.helper import email_msg
from app.decorators import login_require

auth_bp = Blueprint('auth')


class LoginView(BaseView):

    async def post(self, request):
        """
        @api {post} /login Login
        @apiVersion 0.0.1
        @apiName Login-post
        @apiDescription 登录
        @apiGroup Auth

        @apiParam {string} email 邮箱
        @apiParam {string} password 用户密码

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 72
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 0,
            "message": "success",
            "result": {
                "token": "YEmBbhuVQHojIk3cxeWa"
            }
        }

        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 62
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1002,
            "message": "请求参数有误"
        }
        """
        current_user = request.get('current_user')
        if current_user:
            data = {
                "token": request.headers.get('authorization').split(" ")[1]
            }
            return json(Response.make(result=data))
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        email = self.request_arg.get('email')
        password = self.request_arg.get('password')

        user = await User.db_get(email=email)
        if not (user and user.verify_password(password) and user.active):
            return json(Response.make(code=1001), status=400)

        token_str = get_random_str(20)
        await user.gen_confirm_code(request, token=token_str)
        data = {
            "token": token_str
        }

        return json(Response.make(result=data))


class RegisterView(BaseView):

    async def post(self, request):
        """
        @api {post} /register Register
        @apiVersion 0.0.1
        @apiName Register-post
        @apiDescription 注册
        @apiGroup Auth

        @apiParam {string} username  用户名
        @apiParam {string} email 注册邮箱（以后登录使用，单个邮箱只能注册一个帐号）
        @apiParam {string} password 用户密码

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
            "code": 1002,
            "message": "请求参数有误"
        }

        """
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp

        email = self.request_arg.get('email')
        user = await User.db_get(email=email)
        if user:
            return json(Response.make(code=1002), status=400)

        token = get_random_str(20)
        current_user = await User.db_create(**self.request_arg)
        email_status = email_msg(request, email, self.request_arg.get('username'), token)
        if not email_status:
            return json(Response.make(code=1000), starus=400)
        await current_user.gen_confirm_code(request, token)

        return json(Response.make(result='Success'))


class ConfirmView(BaseView):

    async def get(self, request, token):
        """
        @api {post} /confirm/<token> Confirm
        @apiVersion 0.0.1
        @apiName Confirm-get
        @apiDescription 账户邮箱激活
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
            "result":{
                "token":"pwVbZvAAdi8yEaWextkG"
                }
        }


        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 62
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1002,
            "message": "请求参数有误"
        }
        """
        with await request.app.redis as c:
            key, user_id = await c.hmget(token, 'key', 'id')
            user = await User.db_get(id=user_id)
            if not (key.decode() == token and
                    user) or \
                    request.get('current_user') or \
                    user.active:
                return json(Response.make(code=1002), status=401)
        user.active = True
        await user.db_update()
        data = {
            "token": key
        }
        return json(Response.make(result=data))


class ChangeAuthView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request):
        """
        @api {post} /account 修改邮箱
        @apiVersion 0.0.1
        @apiName Confirm-get
        @apiDescription 账户邮箱激活
        @apiGroup Auth

        @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 49
        Content-Type: application/json
        Keep-Alive: 60

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
        HTTP/1.1 400 Bad Request
        Connection: keep-alive
        Content-Length: 62
        Content-Type: application/json
        Keep-Alive: 60

        {
            "code": 1002,
            "message": "请求参数有误",
            "result": {
                "email": [
                    "Missing data for required field."
                ]
            }
        }


        """
        current_user = request.get("current_user")
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp

        email = self.request_arg.get('email')
        password = self.request_arg.get('password')
        exist = await User.db_get(email=email)
        if email == current_user.email and\
                exist:
            return json(Response.make(result="Not Change"))

        with await request.app.redis as coon:
            token = request.headers.get('authorization').split(" ")[1]
            await coon.delete(token)
        current_user.email = email
        current_user.password = password
        current_user.active = False
        update_status = await current_user.db_update()
        if not update_status:
            return json(Response.make(code=1000), status=400)

        token = get_random_str(20)
        email_status = email_msg(request, email, self.request_arg.get('username'), token)
        await current_user.gen_confirm_code(request, token)
        if not email_status:
            return json(Response.make(code=1000), status=400)

        return json(Response.make(result='Success'))


auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(RegisterView.as_view(), '/register')
auth_bp.add_route(ConfirmView.as_view(), '/confirm/<token:[A-Z,a-z,0-9]{20,20}>')
auth_bp.add_route(ChangeAuthView.as_view(), '/account')
