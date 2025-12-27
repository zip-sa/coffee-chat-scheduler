from appserver.libs.datetime.calendar import get_start_weekday_of_month, get_last_day_of_month
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