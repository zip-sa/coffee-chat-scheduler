from datetime import date, timedelta
from tracemalloc import start

# Get the starting weekday of a month (0=Monday, 6=Sunday)
def get_start_weekday_of_month(year, month):
    result = date(year, month, 1)
    return result.weekday()

# Get the last day of a month
def get_last_day_of_month(year, month):
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    result = next_month - timedelta(days=1)
    return result.day

def get_range_days_of_month(year, month):
    # Get the starting weekday (0=Monday, 6=Sunday)
    start_weekday = get_start_weekday_of_month(year, month)

    # Get the last day of the month
    last_day = get_last_day_of_month(year, month)

    # Adjust to make Sunday=0, Saturday=6
    start_weekday = (start_weekday + 1) % 7

    # Prepare the result list with leading zeros for alignment
    result = [0] * start_weekday # fill leading days with 0 before the first day of the month

    # Append the days of the month
    for day in range(1, last_day + 1):
        result.append(day)

    return result