import pytest

from users_api.app import create_app
from users_api.config import TestConfig

from users_api.extensions import db as _db
from users_api.models.posts import Post
from users_api.models.users import User, UserRoles


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(autouse=True)
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()
    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    user = User(email='test@test.com', username='tester', role=UserRoles.ADMIN.value)
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def post(db, user):
    post = Post(user=user, text='Hello, world')
    db.session.add(user)
    db.session.commit()

    return post
