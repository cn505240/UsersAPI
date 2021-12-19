import json
from http import HTTPStatus

import responses


@responses.activate
def test_get_user(client, user, post):
    user_response = client.get(f'/users/{user.id}')

    assert user_response.status_code == HTTPStatus.OK

    user_payload = json.loads(user_response.data)

    assert user_payload['id'] == user.id
    assert user_payload['email'] == user.email
    assert user_payload['username'] == user.username
    assert user_payload['role'] == user.role

    # check that the user's posts came through correctly
    assert len(user_payload['posts']) == 1
    payload_post = user_payload['posts'][0]
    assert payload_post['text'] == post.text


def test_get_user_not_found(client):
    user_response = client.get(f'/users/1')

    assert user_response.status_code == HTTPStatus.NOT_FOUND
