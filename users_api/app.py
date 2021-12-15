from flask import Flask

from users_api.config import Config
from users_api.extensions import db, ma

from users_api.routes.users import blueprint as users_blueprint


def create_app(config_object=Config):
    app = Flask('Users API')
    app.config.from_object(config_object)
    register_extensions(app)
    register_routes(app)
    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)


def register_routes(app):
    app.register_blueprint(users_blueprint)