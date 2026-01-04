from fastapi import status
from fastapi.testclient import TestClient


async def test_signup_successfully(client: TestClient):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "test테스트1234",
        "password_again": "test테스트1234",
    }

    # 회원가입 API 호출
    response = client.post("/account/signup", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["username"] == payload["username"]
    assert isinstance(data["display_name"], str)
    assert len(data["display_name"]) == 8
    assert data["is_host"] is False

    # GET API로 재조회하여 실제로 저장되었는지 확인
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
        "password": "test테스트1234",
        "password_again": "다른비밀번호",
    }

    response = client.post("/account/signup", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

async def test_응답_결과에는_username_display_name_is_host_만_출력한다(client: TestClient):
    payload = {
        "username": "zipsa",
        "display_name": "집사입니다.",
        "email": "test@example.com",
        "password": "test테스트1234",
        "password_again": "test테스트1234",
    }

    response = client.post("/account/signup", json=payload)

    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    response_keys = frozenset(data.keys())
    expected_keys = frozenset(["username", "display_name", "is_host"])
    assert response_keys == expected_keys

