"""
Drug name validation using WHO INN stems.

This module provides utilities to:
- load a WHO stem database from JSON
- analyze drug names to detect stem patterns
- return structured validation results.

Main classes:
- StemDatabase: loads and stores stem definitions
- StemAnalyzer: performs stem detection
- DrugNameValidator: orchestrates validation workflow
"""
import json
from pathlib import Path
from typing import List, Dict


class StemDatabase:
    """
    Loads and manages WHO stem database from JSON file.
    """

    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self._stems = self._load_stems()

    def _load_stems(self) -> Dict[str, str]:
        """
        Load stems from the JSON database and flatten them
        into a single dictionary.
        """
        with open(self.json_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        stems = {}
        for letter_group in raw_data.values():
            stems.update(letter_group)

        return stems

    def get_all_stems(self) -> Dict[str, str]:
        """
        Return the complete dictionary of stems and descriptions.
        """
        return self._stems


class StemMatch:
    """
    Represents a detected stem match.
    """

    def __init__(self, stem: str, description: str):
        self.stem = stem
        self.description = description

    def __str__(self):
        return f"{self.stem} → {self.description}"


class StemAnalyzer:
    """
    Analyzes a drug name against WHO stem database.
    """

    def __init__(self, stem_database: StemDatabase):
        self.stem_database = stem_database

    def analyze(self, drug_name: str) -> List[StemMatch]:
        """
        Analyze a drug name and return matching WHO stems.
        """
        # Ensures case-insensitive detection.
        drug_name = drug_name.lower()
        matches = []
        # iterate through stems
        for stem, description in self.stem_database.get_all_stems().items():

            clean_stem = stem.strip("-")
            # detect stem type
            is_prefix = stem.endswith("-") and not stem.startswith("-")
            is_suffix = stem.startswith("-") and not stem.endswith("-")
            is_infix = stem.startswith("-") and stem.endswith("-")

            if is_suffix and drug_name.endswith(clean_stem):
                matches.append(StemMatch(stem, description))

            elif is_prefix and drug_name.startswith(clean_stem):
                matches.append(StemMatch(stem, description))

            elif is_infix and clean_stem in drug_name:
                matches.append(StemMatch(stem, description))

        return matches


class DrugValidationResult:
    """
    Structured result of validation.
    """

    def __init__(self, drug_name: str, matches: List[StemMatch]):
        self.drug_name = drug_name
        self.matches = matches

    @property
    def is_valid(self) -> bool:
        return len(self.matches) > 0

    def to_dict(self):
        """
        Convert the validation result to a dictionary format.
        """
        return {
            "drug": self.drug_name,
            "valid": self.is_valid,
            "matches": [
                {"stem": m.stem, "description": m.description}
                for m in self.matches
            ],
        }


class DrugNameValidator:
    """
    Main orchestrator class for stem validation.
    """

    def __init__(self, json_path: str):
        self.database = StemDatabase(json_path)
        self.analyzer = StemAnalyzer(self.database)

    def validate(self, drug_name: str) -> DrugValidationResult:
        """
        Validate a drug name against the WHO stem database.
        """
        matches = self.analyzer.analyze(drug_name)
        return DrugValidationResult(drug_name, matches)
