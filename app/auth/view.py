from sanic import Blueprint
from sanic.response import json

from app.models import User, Follow
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
        @api {post} /login 登录
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
        @api {post} /register 注册
        @apiVersion 0.0.1
        @apiName Register
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
        username = self.request_arg.get('username')
        user = await User.db_get(email=email)
        if user or not username:
            return json(Response.make(code=1002), status=400)

        token = get_random_str(20)
        current_user = await User.db_create(**self.request_arg)
        email_status = await email_msg(request, email, self.request_arg.get('username'), token)
        if not email_status:
            return json(Response.make(code=1000), starus=400)
        await current_user.gen_confirm_code(request, token)

        return json(Response.make(result='Success'))


class ConfirmView(BaseView):

    async def get(self, request, token):
        """
        @api {post} /confirm/<token> 用户验证
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
        @api {post} /account 邮箱，密码修改
        @apiVersion 0.0.1
        @apiName Change-auth
        @apiDescription 更改邮箱，密码
        @apiGroup Auth

        @apiParam {string} email 邮箱
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
        update_status = await current_user.db_update(email=email, password=password, active=False)
        if not update_status:
            return json(Response.make(code=1000), status=400)

        token = get_random_str(20)
        email_status = await email_msg(request, email, self.request_arg.get('username'), token)
        await current_user.gen_confirm_code(request, token)
        if not email_status:
            return json(Response.make(code=1000), status=400)

        return json(Response.make(result='Success'))


class FollowView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request, pk):
        """
        @api {post} /follow/<pk:int> 关注用户
        @apiVersion 0.0.1
        @apiName Follow
        @apiDescription 关注某个用户
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
        follow_record = await Follow.db_get(follower=current_user, followed=follow_user)
        result = await current_user.follow(follow_record=follow_record, follow_user=follow_user)

        if not result:
            return json(Response.make(code=1000), status=400)
        return json(Response.make(), status=200)


class LogoutView(BaseView):
    decorators = [login_require('login')]

    async def post(self, request):
        """
        @api {post} /logout 登出
        @apiVersion 0.0.1
        @apiName Logout
        @apiDescription 登出用户
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
        with await request.app.redis as r:
            key = request.app.config.TOKEN_STR + str(current_user.id)
            token = await r.get(key)
            if not token:
                return json(Response.make(code=1002), status=400)

            r.delete(token.decode())
        return json(Response.make())

auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(RegisterView.as_view(), '/register')
auth_bp.add_route(ConfirmView.as_view(), '/confirm/<token:[A-Z,a-z,0-9]{20,20}>')
auth_bp.add_route(ChangeAuthView.as_view(), '/account')
auth_bp.add_route(FollowView.as_view(), '/follow/<pk:int>')
auth_bp.add_route(LogoutView.as_view(), '/logout')
