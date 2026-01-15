import calendar
from datetime import date, timedelta
import pytest

from fastapi import status
from fastapi.testclient import TestClient

from appserver.apps.account.models import User
from appserver.apps.calendar.models import TimeSlot
from appserver.libs.datetime.calendar import get_next_weekday


@pytest.fixture()
def valid_booking_payload(time_slot_tuesday: TimeSlot):
    return {
        "when": get_next_weekday(calendar.TUESDAY).isoformat(),
        "topic": "test",
        "description": "test",
        "time_slot_id": time_slot_tuesday.id,
    }


@pytest.mark.usefixtures("host_user_calendar")
async def test_create_reservation_with_valid_request_returns_http_201_with_reservation_details(
    time_slot_tuesday: TimeSlot,
    host_user: User,
    client_with_guest_auth: TestClient,
    valid_booking_payload: dict
):
    response = client_with_guest_auth.post(
        f"/bookings/{host_user.username}", 
        json=valid_booking_payload
        )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["when"] == valid_booking_payload["when"]
    assert data["topic"] == valid_booking_payload["topic"]
    assert data["description"] == valid_booking_payload["description"]
    assert data["time_slot"]["start_time"] == time_slot_tuesday.start_time.isoformat()
    assert data["time_slot"]["end_time"] == time_slot_tuesday.end_time.isoformat()
    assert data["time_slot"]["weekdays"] == time_slot_tuesday.weekdays


async def test_create_reservation_by_non_host_user_returns_http_404(
        cute_guest_user: User,
        client_with_guest_auth: TestClient,
        valid_booking_payload: dict,
):
    response = client_with_guest_auth.post(
        f"/bookings/{cute_guest_user.username}", 
        json=valid_booking_payload
        )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    
@pytest.mark.parametrize(
    "time_slot_id_add, days_offset",
    [
        (100, 1),  # Non-existent time slot ID
        (0, 2),    # Wednesday - wrong weekday
        (0, 3),    # Thursday - wrong weekday
    ],
)
@pytest.mark.usefixtures("host_user_calendar")
async def test_create_reservation_with_nonexistent_time_slot_returns_http_404(
    host_user: User,
    client_with_guest_auth: TestClient,
    time_slot_tuesday: TimeSlot,
    time_slot_id_add: int,
    days_offset: int,
):
    # Get next Tuesday, then add offset
    next_tuesday = get_next_weekday(calendar.TUESDAY)
    target_date = next_tuesday + timedelta(days=days_offset - 1)

    payload = {
        "when": target_date.isoformat(),
        "topic": "test",
        "description": "test",
        "time_slot_id": time_slot_tuesday.id + time_slot_id_add,
    }

    response = client_with_guest_auth.post(f"/bookings/{host_user.username}", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_host_cannot_book_own_calendar(
    host_user: User,
    client_with_auth: TestClient,
    valid_booking_payload: dict,
):
    response = client_with_auth.post(
        f"/bookings/{host_user.username}", 
        json=valid_booking_payload
        )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

async def test_geust_cannot_book_past(
        host_user: User,
        client_with_auth: TestClient,
        valid_booking_payload: dict,
):
    response = client_with_auth.post(
        f"/bookings/{host_user.username}",
        json=valid_booking_payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
