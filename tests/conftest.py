import pytest

@pytest.fixture
def inn_list():
    with open("data/inn_list.txt") as f:
        return [line.strip() for line in f if line.strip()]
