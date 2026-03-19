"""Tests for stem analysis logic."""
from inn_analyzer.drug_validator import StemDatabase, StemAnalyzer


def test_suffix_detection():
    """Ensure that suffix-based stems (e.g., 'mab') are correctly detected."""
    db = StemDatabase("data/common-stems.json")
    analyzer = StemAnalyzer(db)
    matches = analyzer.analyze("adalimumab")
    assert any("mab" in m.stem for m in matches)
