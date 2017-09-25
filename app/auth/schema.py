import re
from marshmallow import Schema, fields, validates, ValidationError


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String(required=True)
    password = fields.String(load_only=True, required=True)

    @validates('email')
    def validate_email(self, data):
        email = re.match("[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_"
                         "`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", data)
        if not email:
            raise ValidationError('Email is not exit')
