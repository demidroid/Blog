from marshmallow import Schema, fields
from app.users.schema import BaseUserSchema


class BaseBlogSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    like_value = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)


class BlogSchema(Schema):
    last_update_time = fields.DateTime(dump_only=True)


class BlogsSchema(BlogSchema):
    author = fields.Nested(BaseUserSchema, dump_only=True)
