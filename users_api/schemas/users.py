from marshmallow import Schema, fields, validate

from users_api.models.users import UserRoles
from users_api.schemas.posts import PostSchema


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(allow_none=False)
    username = fields.String(allow_none=False)
    role = fields.String(validate=validate.OneOf([role.value for role in UserRoles], error='Invalid user role.'))

    posts = fields.Nested(PostSchema, many=True, dump_only=True)


user_schema = UserSchema()
