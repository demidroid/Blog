from sanic.response import json
from sanic import Blueprint

from app.base import BaseView, PageSchema
from app.utils.http_response import Response
from app.models import Comment
from app.decorators import login_require


comment_bp = Blueprint('comment')


class CommentView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request, blog_id):
        self._check_request(request, PageSchema)
        comments = await Comment.get_by(**self.response_arg, blog=blog_id)
        pass
