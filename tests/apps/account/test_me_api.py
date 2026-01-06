from fastapi import status
from fastapi.testclient import TestClient
from appserver.apps.account.models import User
from appserver.apps.account.utils import decode_token, create_access_token
from datetime import datetime, timedelta, timezone


def test_get_my_info(client_with_auth: TestClient, host_user: User):
    response = client_with_auth.get("/account/@me")

    data = response.json()
    assert response.status_code == status.HTTP_200_OK

    response_key = frozenset(data.keys())
    expected_key = frozenset(["username", "display_name", "is_host", "email", "created_at", "updated_at"])
    assert response_key == expected_key


def test_raises_suspicious_access_error_when_token_missing(client: TestClient):
    response = client.get("/account/@me")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_raises_auth_error_when_token_invalid(client_with_auth: TestClient):
    client_with_auth.cookies["auth_token"] = "invalid_token"
    response = client_with_auth.get("/account/@me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_my_info_with_expired_token(client_with_auth: TestClient):
    token = client_with_auth.cookies.get("auth_token", domain="", path="/")
    decoded = decode_token(token)
    jwt = create_access_token(decoded, timedelta(hours=-1))
    client_with_auth.cookies["auth_token"] = jwt

    response = client_with_auth.get("/account/@me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_my_info_when_user_not_exists(client_with_auth: TestClient):
    token = client_with_auth.cookies.get("auth_token", domain="", path="/")
    decoded = decode_token(token)
    decoded["sub"] = "invalid_user_id"
    jwt = create_access_token(decoded)
    client_with_auth.cookies["auth_token"] = jwt

    response = client_with_auth.get("/account/@me")
    assert response.status_code == status.HTTP_404_NOT_FOUND
