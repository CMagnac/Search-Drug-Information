"""
Tests the WHO stem validation logic.
"""
import time
import pytest
from inn_analyzer.drug_validator import DrugNameValidator


def test_validator_returns_result():
    """Ensure validator returns a result object with the correct drug name."""
    validator = DrugNameValidator("data/common-stems.json")
    result = validator.validate("amoxicillin")
    assert result.drug_name == "amoxicillin"

def test_all_inn_process_without_error(inn_list):
    """Verify all INN entries are processed without errors and match input."""
    validator = DrugNameValidator("data/common-stems.json")
    for drug in inn_list:
        result = validator.validate(drug)
        assert result.drug_name == drug

@pytest.mark.parametrize(
    "drug",
    [
        "adalimumab",
        "rituximab",
        "trastuzumab",
        "bevacizumab",
    ]
)

def test_mab_stem(drug):
    """Check that monoclonal antibody drugs are recognized as valid."""
    validator = DrugNameValidator("data/common-stems.json")
    result = validator.validate(drug)
    assert result.is_valid

def test_percentage_of_valid_stems(inn_list):
    """Ensure that a reasonable proportion of INNs have valid stems."""
    validator = DrugNameValidator("data/common-stems.json")
    valid = 0
    for drug in inn_list:
        if validator.validate(drug).is_valid:
            valid += 1
    coverage = valid / len(inn_list)
    assert coverage > 0.5

def test_validation_speed(inn_list):
    """Ensure validation of all INNs completes within acceptable time."""
    validator = DrugNameValidator("data/common-stems.json")
    start = time.time()
    for drug in inn_list:
        validator.validate(drug)
    duration = time.time() - start
    assert duration < 5
