from fastapi import status
from fastapi.testclient import TestClient
import pytest

from appserver.apps.account.models import User
from appserver.apps.calendar.models import Calendar
from appserver.apps.calendar.schemas import CalendarDetailOut, CalendarOut
from appserver.apps.calendar.endpoints import host_calendar_detail
from appserver.libs.collections.sort import deduplicate_and_sort


@pytest.mark.parametrize("user_key, expected_type", [
    ("host_user", CalendarDetailOut),
    ("guest_user", CalendarOut),
    (None, CalendarOut),
])
async def test_get_calendar_info_by_host_username(
    user_key: str | None,
    expected_type: type[CalendarOut | CalendarDetailOut],
    host_user: User,
    host_user_calendar: Calendar,
    client: TestClient,
    client_with_auth: TestClient,
) -> CalendarOut | CalendarDetailOut:
    clients = {
        "host_user": client_with_auth,
        "guest_user": client,
        None: client,
    }
    user_client = clients[user_key]

    response = user_client.get(f"/calendar/{host_user.username}")
    result = response.json()
    assert response.status_code == status.HTTP_200_OK

    expected_obj = expected_type.model_validate(result)

    assert expected_obj.topics == host_user_calendar.topics
    assert expected_obj.description == host_user_calendar.description
    if isinstance(expected_obj, CalendarDetailOut):
        assert expected_obj.google_calendar_id == host_user_calendar.google_calendar_id


async def test_raise_calendar_info_not_found_error_for_nonexistent_user(client: TestClient) -> None:
    response = client.get("/calendar/not_exist_user")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_raise_calendar_info_not_found_error_for_not_host_user(guest_user: User, client: TestClient) -> None:
    response = client.get(f"/calendar/{guest_user.username}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_host_user_can_create_calendar_with_valid_information(
        host_user: User,
        client_with_auth: TestClient,
) -> None:
    google_calendar_id = "valid_google_calendar_id@group.calendar.google.com"
    payload = {
        "topics" : ["topic2", "topic1", "topic2"],
        "description": "description",
        "google_calendar_id": google_calendar_id,
    }

    response = client_with_auth.post("/calendar", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    result = response.json()
    assert result["host_id"] == host_user.id
    assert result["topics"] == ["topic2", "topic1"]
    assert result["description"] == payload["description"]
    assert result["google_calendar_id"] == payload["google_calendar_id"]


async def test_returns_422_when_calendar_already_exists(
        client_with_auth: TestClient,
) -> None:
    google_calendar_id = "valid_google_calendar_id@group.calendar.google.come"

    payload = {
        "topics" : ["topic2", "topic1", "topic2"],
        "description": "description",
        "google_calendar_id": google_calendar_id,        
    }

    response = client_with_auth.post("/calendar", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    response = client_with_auth.post("/calendar", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_returns_403_when_guest_user_create_calendar(
        client_with_guest_auth: TestClient,
) -> None:
    google_calendar_id = "valid_google_calendar_id@group.calendar.google.come"

    payload = {
        "topics" : ["topic2", "topic1", "topic2"],
        "description": "description",
        "google_calendar_id": google_calendar_id,        
    }

    response = client_with_guest_auth.post("/calendar", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


UPDATABLE_FIELDS = frozenset(["topics", "description", "google_calendar_id"])

@pytest.mark.parametrize("payload", [
    {"topics": ["topic2", "topic1", "topic2"]},
    {"description": "Description text length over 10"},
    {"google_calendar_id": "invalid_google_calendar_id@group.calendar.google.com"},

    {"topics": ["topic2", "topic1", "topic2"], 
     "description": "Description text length over 10", 
     "google_calendar_id": "invalid_google_calendar_id@group.calendar.google.com"}
])
async def test_only_update_values_by_user_changed(
    client_with_auth: TestClient,
    host_user_calendar: Calendar,
    payload: dict,
) -> None:
    before_data = host_user_calendar.model_dump()

    response = client_with_auth.patch("/calendar", json=payload)
    assert response.status_code == status.HTTP_200_OK

    response = client_with_auth.get(f"/calendar/{host_user_calendar.host.username}")
    data = response.json()

    for key, value in payload.items():
        if key == "topics":
            assert data[key] == deduplicate_and_sort(value)
        else:
            assert data[key] == value

    for key in UPDATABLE_FIELDS - frozenset(payload.keys()):
        assert data[key] == before_data[key]
        