from marshmallow import Schema, fields

from app.auth.schema import UserSchema


class BlogSchema(Schema):
    author = fields.Nested(UserSchema, dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    like_value = fields.Integer(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    last_update_time = fields.DateTime(dump_only=True)

