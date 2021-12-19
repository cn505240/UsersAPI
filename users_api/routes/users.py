from http import HTTPStatus

from flask import Blueprint

from users_api.models.users import User
from users_api.schemas.users import user_schema

blueprint = Blueprint('Users Routes', __name__, url_prefix='/users')


@blueprint.route(
    rule='/<int:user_id>',
    methods=['GET']
)
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.dumps(user), HTTPStatus.OK
