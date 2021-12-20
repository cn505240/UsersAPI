import json
from http import HTTPStatus

import pytest

from users_api.models.posts import Post
from users_api.models.users import User, UserRoles


def test_get_user(client, user, post):
    user_response = client.get(f'/users/{user.id}')

    assert user_response.status_code == HTTPStatus.OK

    user_payload = user_response.get_json()
    assert user_payload['id'] == user.id
    assert user_payload['email'] == user.email
    assert user_payload['username'] == user.username
    assert user_payload['role'] == user.role

    # check that the user's posts came through correctly
    assert len(user_payload['posts']) == 1
    payload_post = user_payload['posts'][0]
    assert payload_post['text'] == post.text


def test_get_user_not_found(client):
    user_response = client.get('/users/1')

    assert user_response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(db, client, user, post):
    user_response = client.delete(f'/users/{user.id}')

    assert user_response.status_code == HTTPStatus.NO_CONTENT

    # verify that we removed the user from the DB
    db_user = User.query.filter(User.id == user.id).first()
    assert db_user is None

    # verify that we removed the user's posts from the DB too
    db_post = Post.query.filter_by(user_id=user.id).first()
    assert db_post is None


def test_delete_user_not_found(client):
    user_response = client.delete('/users/1')

    assert user_response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(db, client):
    new_user = {
        'email': 'dayman@sun.com',
        'username': 'champion_of_the_sun',
        'role': 'admin',
    }

    create_user_response = client.post('/users', json=new_user)
    assert create_user_response.status_code == HTTPStatus.CREATED

    # verify the created user is described in the response body
    response_payload = create_user_response.get_json()
    new_user_id = response_payload.get('id')
    assert new_user_id is not None
    assert response_payload['email'] == new_user['email']
    assert response_payload['username'] == new_user['username']
    assert response_payload['role'] == new_user['role']

    # assert that we created a new user in the DB
    db_user = User.query.get(new_user_id)
    assert db_user is not None


@pytest.mark.parametrize(
    ['field', 'value', 'error_message'],
    [
        pytest.param('email', None, 'Field may not be null.'),
        pytest.param('email', 'paddyspub.com', 'Not a valid email address.'),
        pytest.param('username', None, 'Field may not be null.'),
        pytest.param('role', 'elite', 'Invalid user role.'),
    ]
)
def test_create_user_validation_errors(field, value, error_message, client, user):
    new_user = {
        'email': 'nightman@moon.com',
        'username': 'cat_eyes',
        'role': 'admin',
        field: value,
    }
    create_user_response = client.post('/users', json=new_user)

    assert create_user_response.status_code == HTTPStatus.BAD_REQUEST

    res_json = create_user_response.get_json()
    assert res_json['description'] == 'Input failed validation.'
    errors = res_json['errors']['json']
    assert error_message in errors[field]


@pytest.mark.parametrize(
    ['field'],
    [
        pytest.param('email'),
        pytest.param('username'),
    ]
)
def test_create_user_conflicts(field, client, user):
    new_user = {
        'email': 'new@email.com',
        'username': 'new_username',
        'role': 'admin',
        field: getattr(user, field)
    }

    create_user_response = client.post('/users', json=new_user)
    assert create_user_response.status_code == HTTPStatus.CONFLICT


def test_update_user(client, user):
    user_update_payload = {
        'role': UserRoles.BASIC.value
    }

    update_user_response = client.patch(f'/users/{user.id}', json=user_update_payload)
    assert update_user_response.status_code == HTTPStatus.OK

    # check user data returned in response
    response_user = update_user_response.get_json()
    assert response_user['email'] == user.email
    assert response_user['username'] == user.username
    assert response_user['role'] == user_update_payload['role']

    # check DB user data
    db_user = User.query.get(user.id)
    assert db_user.role == user_update_payload['role']


def test_update_user_not_found(client):
    user_update_payload = {
        'role': UserRoles.BASIC.value
    }

    update_user_response = client.patch(f'/users/1', json=user_update_payload)
    assert update_user_response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_input_validation(client, user):
    user_update_payload = {
        'role': 'elite'
    }

    update_user_response = client.patch(f'/users/{user.id}', json=user_update_payload)
    assert update_user_response.status_code == HTTPStatus.BAD_REQUEST

    res_json = update_user_response.get_json()
    assert res_json['description'] == 'Input failed validation.'
    errors = res_json['errors']['json']
    assert errors['role'] == 'Invalid user role.'
