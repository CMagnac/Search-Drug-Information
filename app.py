"""
Drug INN Analyzer web application.

This Streamlit app provides an interface to analyze drug
International Nonproprietary Names (INN). It performs:

1. WHO stem validation using a local stem database.
2. Pharmacology data retrieval from PubChem.

Dependencies:
    - DrugNameValidator: validates INN stems.
    - PubChemClient: retrieves pharmacology sections from PubChem.

The interface allows users to enter a drug name and view
stem classification and pharmacological information.
"""
import streamlit as st

from drug_validator import DrugNameValidator
from pubchem_service import PubChemClient


validator = DrugNameValidator("./DATAS/common-stems.json")
pubchem = PubChemClient()


st.set_page_config(
    page_title="Drug INN Analyzer",
    layout="wide"
)

st.title("Drug INN Analyzer")

st.write(
    "Validate WHO INN stems and retrieve pharmacology information from PubChem."
)


drug_name = st.text_input("Enter drug INN", "amoxicillin")


if st.button("Analyze"):

    if drug_name.strip() == "":
        st.warning("Please enter a drug name.")

    else:

        st.subheader("WHO Stem Validation")

        result = validator.validate(drug_name)

        if result.is_valid:

            st.success("Valid INN stem detected")

            for match in result.matches:

                st.write(f"Stem: **{match.stem}**")
                st.write(match.description)

        else:

            st.error("No WHO stem detected")


        st.subheader("PubChem Pharmacology")


        try:

            data = pubchem.get_pharmacology(drug_name)

            st.write(f"PubChem CID: **{data['cid']}**")

            for section in data["sections"]:

                with st.expander(section["section"]):

                    st.write(section["text"])

        except Exception as e:

            st.warning("Unable to retrieve PubChem pharmacology data.")
            st.exception(e)
