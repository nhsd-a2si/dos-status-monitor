import datetime


def remove_1_hour_from_time_string(current_time: str) -> str:
    """
    Take a time represented as HH:MM string, and return the same format string with 1 hour subtracted
    :param current_time: str
    :return new_time: str
    """
    time_tup = datetime.datetime.strptime(current_time, '%H:%M')
    new_time = time_tup - datetime.timedelta(hours=1)
    return datetime.datetime.strftime(new_time, '%H:%M')

