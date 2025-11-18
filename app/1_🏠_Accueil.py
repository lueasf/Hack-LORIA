# Accueil.py
import streamlit as st

st.set_page_config(
    page_title="Accueil de l'application",
    layout="wide"
)

st.title("Bienvenue sur notre application d'analyse")

st.image("app/assets/accueil.png")

st.markdown("Veuillez choisir l'une des pages ci-dessous pour continuer.")

# Créer des colonnes pour les boutons
col1, col2 = st.columns(2)

with col1:
    st.subheader("🍃 Comparateur d'empreintes carbone de modèles LLM")
    st.write("Envoyez un prompt à plusieurs modèles LLM et comparez leurs réponses et empreintes carbone.")
    if st.button("Aller au comparateur"):
        # Cette fonction change de page programmatiquement
        st.switch_page("pages/3_🍃_Comparateur_d_Empeinte_Carbone_de_LLM.py")

with col2:
    st.subheader("🌍 Calculateur d'Empreinte Carbone")
    st.write("Mesurez l'empreinte carbone de vos scripts.")
    if st.button("Lancer le calculateur"):
        st.switch_page("pages/2_🌍_Calculateur_d_Empreinte_Carbone_De_Code.py")

# La barre latérale affichera également la navigation
st.sidebar.success("Sélectionnez une page ci-dessus.")