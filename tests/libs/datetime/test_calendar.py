from appserver.libs.datetime.calendar import get_start_weekday_of_month, get_last_day_of_month

def test_get_start_weekday_of_month():
    assert get_start_weekday_of_month(2024, 12) == 6
    assert get_start_weekday_of_month(2025, 2) == 5

def test_get_last_day_of_month():
    assert get_last_day_of_month(2024, 2) == 29
    assert get_last_day_of_month(2023, 2) == 28
    assert get_last_day_of_month(2024, 12) == 31
    assert get_last_day_of_month(2024, 11) == 30
