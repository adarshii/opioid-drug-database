# ✅ Cleaned & Optimized Streamlit App for Opioid Drug Database
# Suitable for deployment on Streamlit Cloud

import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors
import requests
import base64
from io import BytesIO

# -----------------------------
# ✅ Opioid Drug Database
# -----------------------------
OPIOID_DATA = [
    {
        "name": "Morphine",
        "iupac": "(5α,6α)-7,8-Didehydro-4,5-epoxy-17-methylmorphinan-3,6-diol",
        "smiles": "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O",
        "formula": "C17H19NO3",
        "weight": 285.34,
        "category": "Natural Opioid",
        "uses": ["Severe pain management", "Palliative care"],
        "toxicity": "High - Respiratory depression, addiction potential",
        "symptoms": ["Drowsiness", "Constipation", "Nausea", "Respiratory depression", "Coma"],
        "side_effects": ["Dependence", "Tolerance", "Withdrawal symptoms"],
        "precautions": ["Avoid alcohol", "Monitor respiratory function", "Risk of addiction"],
        "pubchem_cid": "5288826"
    },
    # Add more drugs if needed...
]

# -----------------------------
# ✅ Utility Functions
# -----------------------------
def get_pubchem_link(cid):
    return f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"

def get_compound_image(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        img = Draw.MolToImage(mol, size=(400, 300))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

def calculate_properties(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {}
    return {
        "Molecular Weight": f"{Descriptors.MolWt(mol):.2f} g/mol",
        "LogP": f"{Descriptors.MolLogP(mol):.2f}",
        "H-Bond Donors": Descriptors.NumHDonors(mol),
        "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
        "Rotatable Bonds": Descriptors.NumRotatableBonds(mol),
        "Polar Surface Area": f"{Descriptors.TPSA(mol):.2f} Å²"
    }

# -----------------------------
# ✅ Home Page
# -----------------------------
def home_page():
    st.title("Opioid Drugs Database")
    st.markdown("""
    Use this app to explore scientific and pharmacological data on commonly used opioid drugs.
    """)

    drug_names = sorted([drug["name"] for drug in OPIOID_DATA])
    selected_drug = st.selectbox("Select an opioid drug:", drug_names)

    if st.button("View Drug Details"):
        st.session_state.current_drug = selected_drug
        st.experimental_rerun()

# -----------------------------
# ✅ Drug Details Page
# -----------------------------
def drug_detail_page():
    drug_name = st.session_state.get("current_drug", "")
    if not drug_name:
        st.error("No drug selected. Please go back to the home page.")
        return

    drug = next((d for d in OPIOID_DATA if d["name"] == drug_name), None)
    if not drug:
        st.error("Drug information not available")
        return

    st.title(f"{drug_name} - Drug Profile")
    st.markdown(f"**Category:** {drug['category']}")

    tab1, tab2 = st.tabs(["Overview", "Chemical Info"])

    with tab1:
        col1, col2 = st.columns([1, 2])

        with col1:
            img_data = get_compound_image(drug["smiles"])
            if img_data:
                st.image(f"data:image/png;base64,{img_data}", caption=f"Structure of {drug_name}")
            st.markdown(f"**IUPAC Name:** {drug['iupac']}")
            st.markdown(f"**Formula:** {drug['formula']}")
            st.markdown(f"**Molecular Weight:** {drug['weight']} g/mol")
            st.markdown(f"[View on PubChem]({get_pubchem_link(drug['pubchem_cid'])})")

        with col2:
            st.subheader("Medical Uses")
            for use in drug["uses"]:
                st.markdown(f"- {use}")

            st.subheader("Precautions")
            for p in drug["precautions"]:
                st.markdown(f"- ⚠️ {p}")

            st.subheader("Toxicity")
            st.markdown(drug["toxicity"])

    with tab2:
        st.subheader("SMILES Notation")
        st.code(drug["smiles"])

        st.subheader("Calculated Properties")
        props = calculate_properties(drug["smiles"])
        for k, v in props.items():
            st.markdown(f"**{k}:** {v}")

        st.subheader("Side Effects")
        for effect in drug["side_effects"]:
            st.markdown(f"- {effect}")

        st.subheader("Overdose Symptoms")
        for s in drug["symptoms"]:
            st.markdown(f"- {s}")

    if st.button("Back to Home"):
        del st.session_state.current_drug
        st.experimental_rerun()

# -----------------------------
# ✅ Main App Logic
# -----------------------------
def main():
    st.set_page_config(
        page_title="Opioid Drug Explorer",
        page_icon="💊",
        layout="wide"
    )

    if "current_drug" not in st.session_state:
        st.session_state.current_drug = None

    if st.session_state.current_drug:
        drug_detail_page()
    else:
        home_page()

if __name__ == "__main__":
    main()

