import pytest
from fastapi import status
from fastapi.testclient import TestClient
from appserver.apps.account.models import User
from sqlalchemy.ext.asyncio import AsyncSession


UPDATABLE_FIELDS = frozenset(["display_name", "email"])


@pytest.mark.parametrize("payload", [
    {"display_name": "zipsahere"},
    {"email": "zipsa@example.com"},
    {"display_name": "zipsahere", "email": "zipsa@example.com"},
])
async def test_update_only_provided_fields_and_keep_others(
    client_with_auth: TestClient,
    payload: dict,
    host_user: User
):
    # Store current user data
    before_data = host_user.model_dump()

    response = client_with_auth.patch("/account/@me", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Updated fields should have new values
    for key, value in payload.items():
        assert data[key] == value

    # Non-updated fields should keep original values
    for key in UPDATABLE_FIELDS - frozenset(payload.keys()):
        assert data[key] == before_data[key]


async def test_require_at_least_one_field_to_update(
    client_with_auth: TestClient,
):
    response = client_with_auth.patch("/account/@me", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_password_should_be_hashed_when_updated(
    client_with_auth: TestClient,
    host_user: User,
    db_session: AsyncSession,
):
    before_password = host_user.hashed_password
    payload = {
        "password": "new_password",
        "password_again": "new_password",
    }

    response = client_with_auth.patch("/account/@me", json=payload)
    assert response.status_code == status.HTTP_200_OK

    await db_session.refresh(host_user)
    assert host_user.hashed_password != before_password


async def test_reject_when_password_mismatch(
    client_with_auth: TestClient,
):
    """Test password and password_again must match"""
    payload = {
        "password": "new_password",
        "password_again": "different_password",
    }

    response = client_with_auth.patch("/account/@me", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("invalid_email", [
    "notanemail",           # Missing @
    "@example.com",         # Missing local part
    "user@",                # Missing domain
    "user@domain",          # Missing TLD
    "user name@domain.com", # Space in email
])
async def test_reject_invalid_email_format(
    client_with_auth: TestClient,
    invalid_email: str,
):
    """Test invalid email formats are rejected"""
    payload = {"email": invalid_email}

    response = client_with_auth.patch("/account/@me", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("invalid_name", [
    "abc",      # Too short (3 chars, min is 4)
    "ab",       # Too short (2 chars)
    "a",        # Too short (1 char)
    "a" * 41,   # Too long (41 chars, max is 40)
    "a" * 50,   # Too long (50 chars)
])
async def test_reject_invalid_display_name_length(
    client_with_auth: TestClient,
    invalid_name: str,
):
    """Test display_name must be between 4-40 characters"""
    payload = {"display_name": invalid_name}

    response = client_with_auth.patch("/account/@me", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_reject_update_without_authentication(
    client: TestClient,
):
    """Test unauthenticated users cannot update profile"""
    payload = {"display_name": "hacker"}

    response = client.patch("/account/@me", json=payload)
    # Should be 422 (token missing) or 401 (unauthorized)
    assert response.status_code in [
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        status.HTTP_401_UNAUTHORIZED
    ]
