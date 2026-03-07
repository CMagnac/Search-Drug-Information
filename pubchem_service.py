import requests


class PubChemClient:

    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest"

    def get_cid(self, drug_name: str):

        url = f"{self.BASE_URL}/pug/compound/name/{drug_name}/cids/JSON"

        r = requests.get(url)
        r.raise_for_status()

        data = r.json()

        return data["IdentifierList"]["CID"][0]

    def get_pharmacology_section(self, cid: int):

        url = f"{self.BASE_URL}/pug_view/data/compound/{cid}/JSON?heading=Pharmacology%20and%20Biochemistry"

        r = requests.get(url)
        r.raise_for_status()

        return r.json()

    def extract_sections(self, data):

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

        cid = self.get_cid(drug_name)

        raw_data = self.get_pharmacology_section(cid)

        return {
            "cid": cid,
            "sections": self.extract_sections(raw_data),
        }
