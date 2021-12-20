from http import HTTPStatus

from flask import Blueprint, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args, parser, abort

from users_api.extensions import db
from users_api.models.users import User
from users_api.schemas.users import user_schema

blueprint = Blueprint('Users Routes', __name__, url_prefix='/users')


@blueprint.route(
    rule='/<int:user_id>',
    methods=['GET']
)
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    print(user.posts)
    return user_schema.dumps(user), HTTPStatus.OK


@blueprint.route(
    rule='/<int:user_id>',
    methods=['DELETE']
)
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)

    return '', HTTPStatus.NO_CONTENT


@blueprint.route(
    rule='',
    methods=['POST']
)
@use_args(user_schema, error_status_code=HTTPStatus.BAD_REQUEST)
def create_user(user):
    try:
        new_user = User(**user)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return 'A user with the same username or email already exists.', HTTPStatus.CONFLICT

    return user_schema.dumps(new_user), HTTPStatus.CREATED


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    response = make_response(
        jsonify(dict(errors=error.messages, description='Input failed validation.')),
        HTTPStatus.BAD_REQUEST
    )
    abort(response)
