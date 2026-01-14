from datetime import date
import pytest

from fastapi import status
from fastapi.testclient import TestClient

from appserver.apps.account.models import User
from appserver.apps.calendar.models import TimeSlot


@pytest.mark.usefixtures("host_user_calendar")
async def test_create_reservation_with_valid_request_returns_http_201_with_reservation_details(
    time_slot_tuesday: TimeSlot,
    host_user: User,
    client_with_guest_auth: TestClient,
):
    target_date = date(2024, 12, 3)
    payload = {
        "when": target_date.isoformat(),
        "topic": "test tuesday topic",
        "description": "this is test tuesday",
        "time_slot_id": time_slot_tuesday.id,
    }

    response = client_with_guest_auth.post(f"/bookings/{host_user.username}", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["when"] == target_date.isoformat()
    assert data["topic"] == "test tuesday topic"
    assert data["description"] == "this is test tuesday"
    assert data["time_slot"]["start_time"] == time_slot_tuesday.start_time.isoformat()
    assert data["time_slot"]["end_time"] == time_slot_tuesday.end_time.isoformat()
    assert data["time_slot"]["weekdays"] == time_slot_tuesday.weekdays


async def test_create_reservation_by_non_host_user_returns_http_404(
        cute_guest_user: User,
        client_with_guest_auth: TestClient,
        time_slot_tuesday: TimeSlot,
):
    target_date = date(2024, 12, 3)
    payload = {
        "when": target_date.isoformat(),
        "topic": "test tuesday topic",
        "description": "this is test tuesday",
        "time_slot_id": time_slot_tuesday.id,
    }
    response = client_with_guest_auth.post(f"/bookings/{cute_guest_user.username}", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    