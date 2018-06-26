import dos_status_monitor.utils as utils


def test_date_and_time_adjusted_correctly_for_bst():

    test_time = "00:20"
    test_date = "12/8/2017"
    result = utils.adjust_timestamp_for_api_bst_bug(test_time, test_date)
    new_time, new_date = result
    assert new_time == "23:20"
    assert new_date == "11/08/2017"


def test_date_and_time_unaltered_if_not_bst():

    test_time = "00:20"
    test_date = "12/12/2017"
    result = utils.adjust_timestamp_for_api_bst_bug(test_time, test_date)
    new_time, new_date = result
    assert new_time == "00:20"
    assert new_date == "12/12/2017"
