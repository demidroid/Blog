from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    followed_value = fields.Integer(dump_only=True)
    follow_value = fields.Integer(dump_only=True)
    gender = fields.Integer()
    create_time = fields.DateTime(dump_only=True)
    last_login_time = fields.DateTime(dump_only=True)
