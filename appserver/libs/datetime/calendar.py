from datetime import date, timedelta

def get_start_weekday_of_month(year, month):
    result = date(year, month, 1)
    return result.weekday()

def get_last_day_of_month(year, month):
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    result = next_month - timedelta(days=1)
    return result.day