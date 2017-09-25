import datetime


def remove_1_hour_from_time_string(current_time: str) -> str:
    # Fix the incorrect service_updated_time by subtracting an hour from the supplied time.
    time_tup = datetime.datetime.strptime(current_time, '%H:%M')
    new_time = time_tup - datetime.timedelta(hours=1)
    return datetime.datetime.strftime(new_time, '%H:%M')
