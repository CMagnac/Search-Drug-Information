from inn_analyzer.drug_validator import StemDatabase


def test_stem_database_loads():
    db = StemDatabase("data/common-stems.json")
    stems = db.get_all_stems()
    assert isinstance(stems, dict)
    assert len(stems) > 0
