import os
from settings import BASE_DIR


def test_file_exists():
    assert os.path.exists(os.path.join(BASE_DIR, '.env'))
