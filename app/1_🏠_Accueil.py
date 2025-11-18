# Accueil.py
import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Accueil de l'application",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger l'image en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Charger l'image de fond
img_path = "app/assets/fond.png"
if os.path.exists(img_path):
    img_base64 = get_base64_image(img_path)
    
    # Appliquer le CSS avec l'image de fond
    st.markdown(f"""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Masquer le header Streamlit (menu, deploy, etc.) mais garder le bouton sidebar */
        #MainMenu {{visibility: hidden;}}
        header {{
            visibility: visible !important;
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        /* Rendre le header toolbar transparent */
        [data-testid="stHeader"] {{
            background: transparent !important;
            background-color: transparent !important;
        }}
        
        footer {{visibility: hidden;}}
        
        /* Forcer le bouton collapse sidebar à toujours être visible */
        [data-testid="collapsedControl"] {{
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: fixed !important;
            left: 0.5rem !important;
            top: 0.5rem !important;
            z-index: 999999 !important;
            background: rgba(255, 255, 255, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        [data-testid="collapsedControl"]:hover {{
            background: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Styliser le bouton toggle de la sidebar */
        button[kind="header"] {{
            display: block !important;
            visibility: visible !important;
            background: rgba(255, 255, 255, 0.25) !important;
            color: #000000 !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        button[kind="header"]:hover {{
            background: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px) !important;
        }}
        
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Rendre la sidebar transparente */
        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        /* Bouton toggle sidebar flottant */
        .sidebar-toggle {{
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 999999;
            background: rgba(255, 255, 255, 0.25) !important;
            color: #000000 !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
            cursor: pointer;
            font-size: 1.5rem;
        }}
        
        .sidebar-toggle:hover {{
            background: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Texte de la sidebar en noir */
        [data-testid="stSidebar"] * {{
            color: #000000 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}
        
        /* Améliorer la lisibilité du texte sur l'image */
        .main .block-container {{
            background: rgba(255, 255, 255, 0.3);
            padding: 2rem;
            border-radius: 20px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        }}
        
        /* Police moderne et texte noir pour tout le contenu */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: #000000 !important;
            font-weight: 700 !important;
        }}
        
        p, div, span, label {{
            color: #000000 !important;
        }}
        
        /* Boutons avec style moderne type Apple liquid */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.25) !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            padding: 0.75rem 2rem !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }}
        
        .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

st.title("Bienvenue sur notre application d'analyse")

st.markdown("Veuillez choisir l'une des pages ci-dessous pour continuer.")

# Créer des colonnes pour les boutons
col1, col2 = st.columns(2)

with col1:
    st.subheader("🍃 PromptCarbon")
    st.write("Mesurez l'empreinte carbone de vos prompts.")
    if st.button("Aller au comparateur"):
        # Cette fonction change de page programmatiquement
        st.switch_page("pages/3_🍃_Comparateur_d_Empeinte_Carbone_de_LLM.py")

with col2:
    st.subheader("🌍 CodeCarbon")
    st.write("Mesurez l'empreinte carbone de vos scripts.")
    if st.button("Lancer le calculateur"):
        st.switch_page("pages/2_🌍_Calculateur_d_Empreinte_Carbone_De_Code.py")

# La barre latérale affichera également la navigation
st.sidebar.success("Sélectionnez une page ci-dessus.")