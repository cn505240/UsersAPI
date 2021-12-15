from flask import Blueprint

blueprint = Blueprint('Users Routes', __name__, url_prefix='/users')


@blueprint.route('/')
def hello():
    return 'Hello world'
