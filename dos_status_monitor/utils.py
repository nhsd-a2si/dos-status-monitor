from datetime import datetime, timedelta
from pytz import reference


def is_bst(time_tup):
    return reference.LocalTimezone().tzname(time_tup) == 'BST'


def adjust_timestamp_for_api_bst_bug(updated_time: str,
                                     updated_date: str) -> (str, str):
    """
    Take a time represented as HH:MM string, and return the same format string with 1 hour subtracted
    :param updated_time: str
    :param updated_date: str
    :return new_time: str
    """

    # The bug only happens during BST
    combined_time = f"{updated_time}-{updated_date}"
    time_tup = datetime.strptime(combined_time, '%H:%M-%d/%m/%Y')

    if is_bst(time_tup):
        print("Is BST")
        new_combined_time = time_tup - timedelta(hours=1)
        new_time = datetime.strftime(new_combined_time, '%H:%M')
        new_date = datetime.strftime(new_combined_time, '%d/%m/%Y')
        return new_time, new_date

    else:
        print("Not BST")
        return updated_time, updated_date
