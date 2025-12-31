import pytest
from pydantic import ValidationError
from unittest import result
from sqlalchemy.ext.asyncio import AsyncSession
from appserver.apps.account.endpoints import signup
from appserver.apps.account.models import User
from fastapi.testclient import TestClient
from appserver.apps.account.exceptions import DuplicatedUsernameError #DuplicatedEmailError

async def test_signup_successfully(client: TestClient, db_session: AsyncSession):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "display_name": "test",
        "password": "test테스트1234",
    }

    result = await signup(payload, db_session)

    assert isinstance(result, User)
    assert result.username == payload["username"]
    assert result.email == payload["email"]
    assert result.display_name == payload["display_name"]
    assert result.is_host is False

    response = client.get(f"/account/users/{payload['username']}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["display_name"] == payload["display_name"]
    assert data["is_host"] is False
    

@pytest.mark.parametrize(
    "username",
    [
        "mynameiszipsamynameiszipsamynameiszipsamynameiszipsamynameiszipsa",
        12345678,
        "x"
    ]
)

async def test_signup_invalid_username(client: TestClient, db_session: AsyncSession, username: str):
    payload = {
        "username": username,
        "email": "test@example.com",
        "display_name": "test",
        "password": "test테스트1234",
    }
    with pytest.raises(ValidationError) as exc:
        await signup(payload, db_session)


async def test_signup_if_id_exists(db_session: AsyncSession):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "display_name": "test",
        "password": "test테스트1234",
    }
    await signup(payload, db_session) 

    payload["email"] = "test2@example.com"
    with pytest.raises(ValidationError) as exc:
        await signup(payload, db_session)