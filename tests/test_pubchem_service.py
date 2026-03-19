"""
Tests the PubChem client.

To ensure tests run without internet access, API calls are mocked using pytest.monkeypath.
This allows the tests to simulate PubChem responses without making real HTTP requests.
"""
from inn_analyzer.pubchem_service import PubChemClient


def test_get_cid(monkeypatch):
    """Test that get_cid returns the expected CID using a mocked API response."""

    def mock_get(_args, _kwargs):
        """Mock requests.get returning a fake PubChem response."""

        class MockResponse:
            """Mock response object mimicking requests.Response."""

            def raise_for_status(self):
                """Simulate successful HTTP response."""
                return None

            def json(self):
                """Return a fake JSON payload."""
                return {"IdentifierList": {"CID": [12345]}}

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    client = PubChemClient()
    cid = client.get_cid("amoxicillin")
    assert cid == 12345

def test_extract_sections():
    """Test extraction of sections from a simulated PubChem response."""
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
    """Test pharmacology retrieval using mocked internal client methods."""
    client = PubChemClient()
    monkeypatch.setattr(client, "get_cid", lambda x: 123)
    monkeypatch.setattr(
        client,
        "get_pharmacology_section",
        lambda x: {"Record": {"Section": []}},
    )
    data = client.get_pharmacology("testdrug")
    assert data["cid"] == 123
