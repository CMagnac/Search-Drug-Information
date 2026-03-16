import pytest
from inn_analyzer.drug_validator import DrugNameValidator


def test_validator_loads():
    validator = DrugNameValidator("data/common-stems.json")
    assert validator is not None

@pytest.mark.parametrize(
    "drug_name",
    ["abacavir", "abafungin", "abagovomab"]
)
def test_validate_known_inn(drug_name):
    validator = DrugNameValidator("data/common-stems.json")
    result = validator.validate(drug_name)
    assert result is not None

def test_all_inn_do_not_crash(inn_list):
    validator = DrugNameValidator("data/common-stems.json")
    for drug in inn_list:
        result = validator.validate(drug)
        assert result is not None
