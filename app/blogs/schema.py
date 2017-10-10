from marshmallow import Schema, fields

from app.auth.schema import UserSchema


class BlogSchema(Schema):
    User = fields.Nested(UserSchema, dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
