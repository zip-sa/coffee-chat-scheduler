from appserver.libs.datetime.calendar import (
    get_start_weekday_of_month, 
    get_last_day_of_month,
    get_range_days_of_month
)
import pytest

@pytest.mark.parametrize("year, month, expected", [
    (2024, 12, 6),
    (2025, 2, 5),
])

def test_get_start_weekday_of_month(year, month, expected):
    """Test get_start_weekday_of_month function."""
    assert get_start_weekday_of_month(year, month) == expected

@pytest.mark.parametrize("year, month, expected", [
    (2024, 2, 29),
    (2025, 2, 28),
    (2024, 4, 30),
    (2024, 12, 31),
])

def test_get_last_day_of_month(year, month, expected):
    """Test get_last_day_of_month function."""
    assert get_last_day_of_month(year, month) == expected

@pytest.mark.parametrize("year, month, expected_padding_count, expected_total_count", [
    # 2024 March: Starts on Friday(5), 31 days
    (2024, 3, 5, 36),
    # 2024 February: Starts on Thursday(4), leap year 29 days
    (2024, 2, 4, 33),
    # 2025 February: Starts on Saturday(6), 28 days
    (2025, 2, 6, 34),
    # 2024 April: Starts on Monday(1), 30 days
    (2024, 4, 1, 31),
    # 2024 December: Starts on Sunday(0), 31 days
    (2024, 12, 0, 31),
])

def test_get_range_days_of_month(year, month, expected_padding_count,
expected_total_count):
    days = get_range_days_of_month(year, month)
    padding_count = days[:expected_padding_count]

    assert sum(padding_count) == 0
    assert days[expected_padding_count] == 1
    assert len(days) == expected_total_count
