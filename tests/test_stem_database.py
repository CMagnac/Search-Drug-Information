"""Tests for the StemDatabase class."""
from inn_analyzer.drug_validator import StemDatabase


def test_stem_database_loads():
    """Ensure the stem database loads correctly and contains data."""
    db = StemDatabase("data/common-stems.json")
    stems = db.get_all_stems()
    assert isinstance(stems, dict)
    assert len(stems) > 0
