from datetime import date, timedelta


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


from datetime import date, timedelta

def get_next_weekday(weekday: int, start_date: date = None) -> date:
    """
    Returns the nearest date that matches the given weekday,
    based on the provided start date.

    If no start date is given, today’s date is used as the reference.
    If the start date already falls on the given weekday,
    the start date itself is returned.

    :param weekday: Target weekday (0=Monday, 6=Sunday)
    :param start_date: Reference date (default: today)
    :return: The nearest date matching the given weekday

    >>> import calendar
    >>> from datetime import date
    >>> target_date = date(2024, 12, 1)
    >>> get_next_weekday(calendar.MONDAY, target_date)
    datetime.date(2024, 12, 2)
    >>> get_next_weekday(calendar.TUESDAY, target_date)
    datetime.date(2024, 12, 3)
    >>> get_next_weekday(calendar.WEDNESDAY, target_date)
    datetime.date(2024, 12, 4)
    """
    if start_date is None:
        start_date = date.today()

    days_ahead = (weekday - start_date.weekday() + 7) % 7
    if days_ahead == 0:
        return start_date
    else:
        return start_date + timedelta(days=days_ahead)
