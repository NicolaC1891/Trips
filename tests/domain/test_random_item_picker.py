from domain.random_picker import RandomItemPicker


def test_result_is_consistent():
    """
    Tests that repeatable results of class method are consistent.
    """
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    picker = RandomItemPicker(items)
    result_1 = picker.pick_by_seed_today()
    result_2 = picker.pick_by_seed_today()
    assert result_1 == result_2
    assert result_1 in items
