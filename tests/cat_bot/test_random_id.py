import pytest

from cat_bot.daily_wisdom import get_daily_random_id


@pytest.fixture
def get_test_ids():
    test_ids = [12345, 234567890, 3123123123123, 404040404, 55]
    return test_ids


def test_get_daily_random_id(get_test_ids):
    test_id = get_daily_random_id(get_test_ids)
    assert isinstance(test_id, int)


def test_daily_id_is_consistent(get_test_ids):
    test_id_1 = get_daily_random_id(get_test_ids)
    test_id_2 = get_daily_random_id(get_test_ids)
    assert test_id_1 == test_id_2


def test_daily_id_is_from_source(get_test_ids):
    test_id = get_daily_random_id(get_test_ids)
    assert test_id in get_test_ids


def test_does_not_process_empty_list():  # Processed in upper level func
    test_ids = []
    with pytest.raises(IndexError):  # Error is expected
        get_daily_random_id(test_ids)
