import pytest
from dos_status_monitor.config import config_string_to_bool

test_strings = [('true', True),
                ('TRUE', True),
                ('True', True),
                ('false', False),
                ('FALSE', False),
                ('False', False),
                ('yes', True),
                ('YES', True),
                ('Yes', True),
                ('no', False),
                ('NO', False),
                ('No', False),
                ('jam', False),
                ('Affirmative', False),
                ('', False)]


@pytest.mark.parametrize("test_data", test_strings)
def test_config_string_converts_to_bool_correctly(test_data):

    result = config_string_to_bool(test_data[0])
    assert result is test_data[1]
