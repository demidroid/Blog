from marshmallow import Schema, fields


class PageSchema(Schema):
    page = fields.Integer(missing=1)
    count = fields.Integer(missing=10)
    desc = fields.Integer(missing=0)
    sort = fields.String(missing='create_time')
