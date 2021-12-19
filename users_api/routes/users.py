from flask import Blueprint

from users_api.extensions import db
from users_api.models.users import User, UserRoles

blueprint = Blueprint('Users Routes', __name__, url_prefix='/users')


@blueprint.route('')
def create_user():
    user = User(email='test@test.com', username='tester', role=UserRoles.ADMIN)
    db.session.add(user)
    db.session.commit()
    return 'Created a user!'
