"""Pytest fixtures for loading INN test data."""
import pytest

@pytest.fixture
def inn_list():
    """Load and return a list of non-empty INN values from a text file."""
    with open("data/inn_list.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
