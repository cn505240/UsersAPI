from http import HTTPStatus


def test_get_user(app, user):
    user_response = app.get(f'/users/{user.id}')

    assert user_response.status_code == HTTPStatus.OK

    user_payload = user_response.json()
    assert user_payload['id'] == user.id
    assert user_payload['email'] == user.email
    assert user_payload['username'] == user.username
    assert user_payload['role'] == user.role
