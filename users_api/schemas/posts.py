from marshmallow import fields, Schema


class PostSchema(Schema):
    id = fields.Integer()
    text = fields.String()

