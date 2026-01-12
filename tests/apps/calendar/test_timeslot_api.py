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


@pytest.mark.parametrize("start_time, end_time, weekdays, expected_status_code", [
    # Non-overlapping cases
    (time(9, 0), time(10,0), [calendar.MONDAY], status.HTTP_201_CREATED),
    (time(9, 0), time(10,0), [calendar.MONDAY], status.HTTP_201_CREATED),
    (time(9, 0), time(10,0), [calendar.MONDAY], status.HTTP_201_CREATED),

    # Overlapping cases (same weekday)
    (time(10, 30), time(11, 30), [calendar.MONDAY], status.HTTP_422_UNPROCESSABLE_ENTITY),
    (time(9, 30), time(10, 30), [calendar.MONDAY], status.HTTP_422_UNPROCESSABLE_ENTITY),
    (time(10, 0), time(11, 0), [calendar.MONDAY], status.HTTP_422_UNPROCESSABLE_ENTITY),

    # Non-overlapping cases (different weekdays)
    (time(10, 0), time(11,0), [calendar.THURSDAY], status.HTTP_201_CREATED),
    (time(10, 0), time(11,0), [calendar.FRIDAY], status.HTTP_201_CREATED),
])
@pytest.mark.usefixtures("host_user_calendar")
async def test_returns_422_when_timeslots_overlap(
    client_with_auth: TestClient,
    start_time: time,
    end_time: time,
    weekdays: list[int],
    expected_status_code: int,
):
    # Create first timeslot
    payload = {
        "start_time": time(10, 0).isoformat(),
        "end_time": time(11,0).isoformat(),
        "weekdays": [calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY],
    }
    response = client_with_auth.post("/time-slots", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Create second timeslot with test parameters
    payload = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "weekdays": weekdays
    }
    response = client_with_auth.post("/time-slots", json=payload)
    assert response.status_code == expected_status_code
