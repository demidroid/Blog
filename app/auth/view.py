from sanic import Blueprint
from sanic.response import json, html

from app.models import User
from app.base import BaseView
from app.utils import Response
from .schema import UserSchema
from app.utils.security import generate_password, verify_password, get_random_str
from app.utils.helper import email_msg

auth_bp = Blueprint('auth')


class LoginView(BaseView):

    async def get(self, request):
        return html('<h1>Login</h1>')

    async def post(self, request):
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        email = self.request_arg.get('email')
        password = self.request_arg.get('password')

        user = await User.db_get(email=email)
        if not (user and verify_password(password, user.password) and user.active):
            return json(Response.make(code=1001), status=400)

        self._check_data(user, UserSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))


class RegisterView(BaseView):

    async def get(self, request):
        return html('<h1>Register</h1>')

    async def post(self, request):
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        email = self.request_arg.get('email')
        token = get_random_str(20)
        email_status = email_msg(request, email, self.request_arg.get('username'), token)

        user = await User.db_get(email=email)
        if user or not email_status:
            return json(Response.make(code=1002), status=400)

        current_user = await User.db_create(**self.request_arg)
        await current_user.gen_confirm_code(request, token)

        return json(Response.make(result='Success'))


class ConfirmView(BaseView):

    async def get(self, request, token):
        with await request.app.redis as c:
            key, user_id = await c.hmget(token, 'key', 'id')
            user = await User.db_get(id=user_id)
            if not (key.decode() == token and
                    user) or \
                    request.get('current_user') or \
                    user.active:
                return json(Response.make(code=1002), status=401)
        await user.db_update(pk=user.id, active=True)
        data = {
            "token": key
        }
        return json(Response.make(result=data))

auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(RegisterView.as_view(), '/register')
auth_bp.add_route(ConfirmView.as_view(), '/confirm/<token>')
