from datetime import time
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import calendar

@pytest.mark.usefixtures("host_user_calendar")
async def test_host_user_can_create_timeslot_with_valid_information(
    client_with_auth: TestClient,
):
    payload = {
        "start_time": time(10,0).isoformat(),
        "end_time": time(11, 0).isoformat(),
        "weekdays": [calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY],
    }

    response = client_with_auth.post(
        "/time-slots",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.usefixtures("host_user_calendar")
async def test_creating_timeslot_with_invalid_data_returns_422(
    client_with_auth: TestClient,
):
    payload = {
        "start_time": time(11,0).isoformat(),
        "end_time": time(10, 0).isoformat(),
        "weekdays": [calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY],
    }

    response = client_with_auth.post(
        "/time-slots",
        json=payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("weekdays", [
    [-1, 0, 1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7],
])
@pytest.mark.usefixtures("host_user_calendar")
async def test_weekdays_are_zero_indexed_from_monday_to_sunday(
    client_with_auth: TestClient,
    weekdays: list[int],
):
    payload = {
        "start_time": time(10,0).isoformat(),
        "end_time": time(11, 0).isoformat(),
        "weekdays": weekdays,
    }

    response = client_with_auth.post(
        "/time-slots",
        json=payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    