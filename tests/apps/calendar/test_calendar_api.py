from fastapi import status
from fastapi.testclient import TestClient
import pytest

from appserver.apps.account.models import User
from appserver.apps.calendar.models import Calendar
from appserver.apps.calendar.schemas import CalendarDetailOut, CalendarOut
from appserver.apps.calendar.endpoints import host_calendar_detail


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
