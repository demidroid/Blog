class Response:
    success_0 = {
        "code": 0,
        "message": "success"
    }

    error_1000 = {
        "code": 1000,
        "message": "系统错误"
    }

    error_1001 = {
        "code": 1001,
        "message": "账号或密码错误"
    }

    error_1002 = {
        "code": 1002,
        "message": "请求参数有误"
    }

    error_1003 = {
        "code": 1003,
        "message": "权限不足"
    }

    error_1004 = {
        "code": 1004,
        "message": "数据库错误"
    }

    system_404 = {
        "code": 404,
        "message": "Not Found"
    }

    @classmethod
    def make(cls, code=0, message=None, **kwargs):
        if int(code) == 0:
            response = getattr(cls, 'success_0')
        elif 100 < int(code) < 800:
            response = getattr(cls, 'system_' + str(code))
        else:
            response = getattr(cls, 'error_' + str(code))

        if message is not None:
            response['message'] = message

        if kwargs:
            response.update(kwargs)

        return response

    def __getattr__(self, item):
        return self.error_1000
