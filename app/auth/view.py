from sanic import Blueprint
from sanic.response import json, html

from app.models import User
from app.base import BaseView
from app.utils import Response
from .schema import UserSchema
from app.utils.security import generate_password, verify_password

auth_bp = Blueprint('auth')


class LoginView(BaseView):

    async def get(self, request):
        return html('<h1>Login</login>')

    async def post(self, request):
        self._check_request(request, UserSchema)
        if self.error:
            return self.error_resp
        email = self.request_arg.get('email')
        password = self.request_arg.get('password')

        user = await User.db_get(email=email)
        if not user or not verify_password(password, user.password):
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

        user = await User.db_get(email=email)
        if user:
            return json(Response.make(code=1005), status=400)

        password = generate_password(self.request_arg.get('password'))
        self.request_arg.update({
            "password": password
        })

        current_user = await User.db_create(**self.request_arg)

        self._check_data(current_user, UserSchema())
        if self.error:
            return self.error_resp

        return json(Response.make(result=self.response_arg))


auth_bp.add_route(LoginView.as_view(), '/login')
auth_bp.add_route(RegisterView.as_view(), '/register')
