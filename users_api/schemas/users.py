from marshmallow import Schema, fields, validate

from users_api.models.users import UserRoles
from users_api.schemas.posts import PostSchema


class UserRoleSchema(Schema):
    role = fields.String(validate=validate.OneOf([role.value for role in UserRoles], error='Invalid user role.'))


class UserSchema(UserRoleSchema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(allow_none=False)
    username = fields.String(allow_none=False)

    posts = fields.Nested(PostSchema, many=True, dump_only=True)


user_schema = UserSchema()
user_role_schema = UserRoleSchema()
