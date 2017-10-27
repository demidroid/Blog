from sanic.response import json
from sanic import Blueprint

from app.base import BaseView, PageSchema
from app.utils.http_response import Response
from app.models import Comment, Blog
from app.blogs.schema import BlogsSchema
from .schema import CommentSchema
from app.decorators import login_require


comment_bp = Blueprint('comment')


class CommentsView(BaseView):
    decorators = [login_require('login')]

    async def get(self, request, blog_id):
        self._check_request(request, PageSchema)
        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)
        comments = await Comment.get_by(**self.response_arg, blog=blog)
        self._check_data(blog, BlogsSchema())
        if self.error:
            return self.error_resp
        result = {"blog": self.response_arg}
        self._check_data(comments, CommentSchema(many=True))
        if self.error:
            return self.error_resp
        result.update({"comments": self.response_arg})
        return json(Response.make(result=result))

    async def post(self, request, blog_id):
        self._check_request(request, CommentSchema)
        if self.error:
            return self.error_resp

        blog = await Blog.db_get(id=blog_id, is_delete=False)
        if not blog:
            return json(Response.make(code=1005), status=400)
        author = request.get('current_user')

        comment = await Comment.db_create(blog=blog, author=author, is_delete=False, **self.request_arg)
        if not comment:
            return json(Response.make(code=1004), status=400)

        return await self.get(request, blog_id)

    async def patch(self, request):
        pass


class CommentView(BaseView):
    decorators = [login_require('login')]

    async def delete(self, request, comment_id):
        comment = await Comment.db_get(id=comment_id)
        if not comment.author == request.get('current_user'):
            return json(Response.make(code=1003), status=400)
        await comment.db_update(is_delete=True)
        return json(Response.make())

comment_bp.add_route(CommentsView.as_view(), "/<blog_id:int>/comments")
comment_bp.add_route(CommentView.as_view(), "/comments/<comment_id:int>")
