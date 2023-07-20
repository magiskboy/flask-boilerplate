import pytest
from app.extensions.login_manager import jwt_decode


def send_request(client, data):
    return client.post("/api/auth/login", json=data)


@pytest.mark.parametrize("data,field_errors", [
    ({"username": 1, "password": 1}, ["username", "password"]),
    ({"username": "username", "password": 1}, ["password"]),
    ({"username": 1, "password": "password"}, ["username"]),
    ({"username": "username", "password": None}, ["password"]),
    ({"username": None, "password": "password"}, ["username"]),
])
def test_with_invalid_request(client, data, field_errors):
    res = send_request(client, data)
    assert res.status_code == 400
    assert "errors" in res.json

    actual_field_errors = [e["loc"] for e in res.json["errors"]]
    assert sorted(actual_field_errors) == sorted(field_errors)


def test_with_invalid_credential(client, faker):
    password = faker.password()
    user = faker.user(password=password)

    request = {
        "username": user.username,
        "password": faker.password(),
    }
    res = send_request(client, request)

    assert res.status_code == 401


def test_with_valid_request(client, faker):
    password = faker.password()
    user = faker.user(password=password)

    request = {
        "username": user.username,
        "password": password,
    }
    res = send_request(client, request)

    assert res.status_code == 200
    assert "token" in res.json

    payload = jwt_decode(res.json["token"])
    assert isinstance(payload, dict)
    assert payload.get("id") == user.id_
    assert payload.get("username") == user.username
    assert payload.get("role") == user.role
