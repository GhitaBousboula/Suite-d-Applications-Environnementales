import streamlit as st
from apps import leopold, AI1, AI2

# Configuration
st.set_page_config(
    page_title="Suite d'Applications Environnementales", 
    page_icon="🌍",
    layout="wide"
)

APPLICATIONS = {
    "🌍 Générateur de Matrice": {
        "module": leopold,
        "description": "Générateur de matrice d'impact environnemental"
    },
    "🛣️ Assistant IA - Évaluation Environnementale Autoroutière": {
        "module": AI1,
        "description": "IA pour impacts et mesures d'atténuation"
    },
    "🛰️ Monitoring Télédétection": {
        "module": AI2,
        "description": "Analyse satellite avec Sentinel-1 et GEEMAP"
    }
}

# Navigation sidebar
st.sidebar.title("🌍 Navigation")
st.sidebar.markdown("---")

selected_app = st.sidebar.selectbox(
    "Choisir une application:",
    list(APPLICATIONS.keys())
)

# Affichage sécurisé
if selected_app in APPLICATIONS:
    st.sidebar.info(APPLICATIONS[selected_app]["description"])
    st.sidebar.markdown("---")
    
    # CORRECTION : Accéder au module via la clé "module"
    APPLICATIONS[selected_app]["module"].run()

    #                         ^^^^^^^^^^
