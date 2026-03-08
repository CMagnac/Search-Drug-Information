"""
Client for retrieving pharmacology data from PubChem.

This module provides a simple wrapper around the PubChem REST API
to retrieve compound identifiers (CID) and pharmacology sections
for a given drug name.
"""
import requests


class PubChemClient:
    """
    Client for interacting with the PubChem REST API.
    Provides methods to:
    - retrieve a compound CID from a drug name
    - fetch pharmacology sections
    - extract readable pharmacology information
    """
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest"

    def get_cid(self, drug_name: str):
        """
        Retrieve the PubChem CID for a given drug name.
        """
        url = f"{self.BASE_URL}/pug/compound/name/{drug_name}/cids/JSON"

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        return data["IdentifierList"]["CID"][0]

    def get_pharmacology_section(self, cid: int):
        """
        Retrieve the pharmacology and biochemistry section
        for a compound using its CID.
        """
        url = f"{self.BASE_URL}/pug_view/data/compound/{cid}/JSON?heading=Pharmacology%20and%20Biochemistry"

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        return r.json()

    def extract_sections(self, data):
        """
        Extract pharmacology sections from the PubChem JSON response.
        """
        sections = []

        def parse(section):

            title = section.get("TOCHeading")

            if "Information" in section:

                for info in section["Information"]:

                    if "Value" in info and "StringWithMarkup" in info["Value"]:

                        text = " ".join(
                            item["String"]
                            for item in info["Value"]["StringWithMarkup"]
                        )

                        sections.append(
                            {
                                "section": title,
                                "text": text,
                            }
                        )

            if "Section" in section:
                for sub in section["Section"]:
                    parse(sub)

        for section in data["Record"]["Section"]:
            parse(section)

        return sections

    def get_pharmacology(self, drug_name: str):
        """
        Retrieve pharmacology information for a drug name.
        """
        cid = self.get_cid(drug_name)

        raw_data = self.get_pharmacology_section(cid)

        return {
            "cid": cid,
            "sections": self.extract_sections(raw_data),
        }
