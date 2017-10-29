from marshmallow import fields, Schema
from app.users.schema import BaseUserSchema


class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    author = fields.Nested(BaseUserSchema, dump_only=True)
    content = fields.String()
    like_value = fields.Integer(dump_only=True)
    is_delete = fields.Boolean(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    blog = fields.Integer(dump_only=True)
