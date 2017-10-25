from marshmallow import fields, Schema


class BaseUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    followed_value = fields.Integer(dump_only=True)
    follow_value = fields.Integer(dump_only=True)
    gender = fields.Integer()


class UserSchema(BaseUserSchema):
    create_time = fields.DateTime(dump_only=True)
    last_login_time = fields.DateTime(dump_only=True)


class MyInfoSchema(UserSchema):
    email = fields.String(dump_only=True)


