import enum

from users_api.extensions import db


class UserRoles(enum.Enum):
    BASIC = 'basic'
    ADMIN = 'admin'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    role = db.Column(db.String(30))

    posts = db.relationship('Post', backref='user')
