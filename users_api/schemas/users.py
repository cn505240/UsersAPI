from marshmallow import Schema, fields, validate

from users_api.models.users import UserRoles


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    username = fields.String()
    role = fields.String(validate=validate.OneOf(role.value for role in UserRoles))


user_schema = UserSchema()
