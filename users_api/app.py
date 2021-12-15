from flask import Flask

from users_api.config import Config
from users_api.extensions import db, ma


def create_app(config_object=Config):
    app = Flask('Users API')
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
