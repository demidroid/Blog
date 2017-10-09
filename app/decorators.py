from functools import wraps
from sanic.response import json
from app.utils.http_response import Response


def login_require(permission):
    def auth_login(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if args:
                request = args[0]
                if not request.get('current_user') and permission.upper() == 'LOGIN':
                    return json(Response.make(code=1001), status=401)

            return f(*args, **kwargs)
        return decorator
    return auth_login
