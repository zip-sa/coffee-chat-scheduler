from datetime import date, timedelta
from tracemalloc import start


def get_start_weekday_of_month(year, month):
    """
    Get the starting weekday of a month (0=Monday, 6=Sunday)
    
    >>> get_start_weekday_of_month(2024, 12)
    6
    >>> get_start_weekday_of_month(2025, 2)
    5
    """
    return date(year, month, 1).weekday()

def get_last_day_of_month(year, month):
    """
    Get the last day of a month.

    >>> get_last_day_of_month(2024, 2)
    29
    >>> get_last_day_of_month(2025, 2)
    28
    >>> get_last_day_of_month(2024, 4)
    30
    >>> get_last_day_of_month(2024, 12)
    31
    """
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    result = next_month - timedelta(days=1)
    return result.day

def get_range_days_of_month(year, month):
    """
    Get days of the month
    
    >>> result = get_range_days_of_month(2024, 3)
    >>> result[:5]
    [0, 0, 0, 0, 0]
    >>> result[5]
    1
    >>> len(result)
    36
    >>> result = get_range_days_of_month(2024, 2) # Leap year
    >>> result[:4]
    [0, 0, 0, 0]
    >>> result[4]
    1
    >>> len(result)
    33
    """

    # Get the starting weekday (0=Monday, 6=Sunday)
    start_weekday = get_start_weekday_of_month(year, month)

    # Get the last day of the month
    last_day = get_last_day_of_month(year, month)

    # Adjust to make Sunday=0, Saturday=6
    start_weekday = (start_weekday + 1) % 7

    # Prepare the result list with leading zeros for alignment
    result = [0] * start_weekday # fill leading days with 0 before the first day of the month

    # Append the days of the month
    # for day in range(1, last_day + 1):
    #   result.append(day)

    return result + list(range(1, last_day + 1))