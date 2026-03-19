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

from inn_analyzer.drug_validator import DrugNameValidator
from inn_analyzer.pubchem_service import PubChemClient

# Initialize services
validator = DrugNameValidator("./data/common-stems.json")
pubchem = PubChemClient()

def analyze_drug(drug_name: str):
    """
    Perform stem validation and PubChem retrieval.
    """
    result = validator.validate(drug_name)
    pharmacology = pubchem.get_pharmacology(drug_name)

    return result, pharmacology


def main():
    # Streamlit configuration
    st.set_page_config(
        page_title="Drug INN Analyzer",
        layout="wide"
    )
    st.title("Drug INN Analyzer")
    st.write("Validate WHO INN stems and retrieve pharmacology information from PubChem.")
    # Creates an input box with default value amoxicillin.
    drug_name = st.text_input("Enter drug INN", "amoxicillin")
    # The analysis runs only when the button is pressed.
    if st.button("Analyze"):
        # Prevents empty input.
        if not drug_name.strip():
            st.warning("Please enter a drug name.")
            return

        result, data = analyze_drug(drug_name)
        st.subheader("WHO Stem Validation")

        if result.is_valid:
            st.success("Valid INN stem detected")

            for match in result.matches:
                st.write(f"Stem: **{match.stem}**")
                st.write(match.description)

        else:
            st.error("No WHO stem detected")
        st.subheader("PubChem Pharmacology")
        st.write(f"PubChem CID: **{data['cid']}**")

        for section in data["sections"]:
            with st.expander(section["section"]):
                st.write(section["text"])


if __name__ == "__main__":
    main()
