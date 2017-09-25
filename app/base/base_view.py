from sanic.views import HTTPMethodView
from sanic.log import log
from sanic.response import json
from app.utils import Response
from app.utils.helper import data_dumps, request_loads


class BaseView(HTTPMethodView):
    logger = log
    request_arg = dict()
    error = dict()
    error_resp = Response.make(code=1002)
    response_arg = list() or dict()

    def _check_request(self, request, schema):
        data, error = request_loads(request, schema)
        if error:
            self.error = error
            self.error_resp = json(Response.make(code=1002, result=error), status=400)
        self.request_arg = data

    def _check_data(self, data, schema):
        result, error = data_dumps(data, schema)
        if error:
            self.error = error
            self.error_resp = json(Response.make(code=1002, result=error), status=400)
        self.response_arg = result

