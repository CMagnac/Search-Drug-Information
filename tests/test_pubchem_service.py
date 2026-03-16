"""
Tests the PubChem client.

To ensure tests run without internet access, API calls are mocked using pytest.monkeypath.
This allows the tests to simulate PubChem responses without making real HTTP requests.
"""
from inn_analyzer.pubchem_service import PubChemClient


def test_get_cid(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self):
                return {"IdentifierList": {"CID": [12345]}}
        return MockResponse()
    monkeypatch.setattr("requests.get", mock_get)
    client = PubChemClient()
    cid = client.get_cid("amoxicillin")
    assert cid == 12345

def test_extract_sections():
    client = PubChemClient()
    fake_data = {
        "Record": {
            "Section": [
                {
                    "TOCHeading": "Mechanism",
                    "Information": [
                        {
                            "Value": {
                                "StringWithMarkup": [
                                    {"String": "Drug mechanism description"}
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
    sections = client.extract_sections(fake_data)
    assert sections[0]["section"] == "Mechanism"

def test_get_pharmacology_mock(monkeypatch):

    client = PubChemClient()
    monkeypatch.setattr(client, "get_cid", lambda x: 123)
    monkeypatch.setattr(
        client,
        "get_pharmacology_section",
        lambda x: {"Record": {"Section": []}},
    )
    data = client.get_pharmacology("testdrug")
    assert data["cid"] == 123
