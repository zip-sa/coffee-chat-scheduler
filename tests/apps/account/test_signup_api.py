from fastapi import status
from fastapi.testclient import TestClient


async def test_signup_successfully(client: TestClient):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "testTest1234",
        "password_again": "testTest1234",
    }

    # Call signup API
    response = client.post("/account/signup", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["username"] == payload["username"]
    assert isinstance(data["display_name"], str)
    assert len(data["display_name"]) == 8
    assert data["is_host"] is False

    # Verify saved by re-querying with GET API
    response = client.get(f"/account/users/{payload['username']}")
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["username"] == payload["username"]
    assert user_data["email"] == payload["email"]
    assert user_data["display_name"] == data["display_name"]


async def test_signup_password_mismatch(client: TestClient):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "testTest1234",
        "password_again": "differentPassword",
    }

    response = client.post("/account/signup", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

async def test_response_contains_only_username_display_name_is_host(client: TestClient):
    payload = {
        "username": "zipsa",
        "display_name": "zipsahere",
        "email": "test@example.com",
        "password": "testTest1234",
        "password_again": "testTest1234",
    }

    response = client.post("/account/signup", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    response_keys = frozenset(data.keys())
    expected_keys = frozenset(["username", "display_name", "is_host"])
    assert response_keys == expected_keys

