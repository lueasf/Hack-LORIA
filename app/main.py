# main.py
import streamlit as st

# 1. CONFIGURATION
st.set_page_config(layout="wide", page_title="TelecomCarbon")

# 2. CHARGEMENT CSS GLOBAL
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("app/accueil_styles.css")

# 3. --- LE CSS CORRIGÉ (VISUEL + CLICS) ---
st.markdown("""
    <style>
        /* --- 1. SUPPRESSION PHYSIQUE DES ÉLÉMENTS PAR DÉFAUT --- */
        /* IMPORTANT : display: none supprime l'élément du flux. 
           visibility: hidden le laissait là (et bloquait les clics). */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        .stAppDeployButton {
            display: none !important;
        }
        
        /* --- 2. LA BARRE DE NAVIGATION (NAVBAR) --- */
        div[data-testid="stHorizontalBlock"]:has(.nav-logo) {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            /* Z-index très élevé pour passer au-dessus de TOUT (graphes, cartes, etc.) */
            z-index: 999999 !important; 
            
            /* STYLE VISUEL (Dark Glass) */
            background: rgba(15, 15, 15, 0.90); /* Un peu plus opaque pour la lisibilité */
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            
            padding: 1.5rem 3rem;
            margin: 0;
            border-radius: 0;
            gap: 2rem;
        }

        /* --- 3. GESTION DU CONTENU SOUS LA BARRE --- */
        /* On pousse le contenu vers le bas pour qu'il ne soit pas caché sous la barre fixe */
        .main .block-container {
            margin-top: 4rem !important; 
            padding-top: 2rem !important;
        }

        /* --- 4. STYLE DU LOGO --- */
        .nav-logo {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            margin: 0 !important;
            pointer-events: none; /* Le texte du logo ne gêne pas les clics */
        }

        /* --- 5. STYLE DES BOUTONS --- */
        /* Cible spécifique pour rendre les liens bien cliquables */
        div[data-testid="stHorizontalBlock"]:has(.nav-logo) a {
            z-index: 1000000 !important; /* Encore plus haut que la barre */
            position: relative;
        }

        div[data-testid="stHorizontalBlock"]:has(.nav-logo) p {
            color: #e0e0e0 !important;
            font-weight: 500;
            margin: 0;
        }
        
        /* Effet au survol des boutons */
        div[data-testid="stHorizontalBlock"]:has(.nav-logo) div[data-testid="stPageLink-NavLink"]:hover {
            background-color: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-1px);
        }

    </style>
""", unsafe_allow_html=True)

# 4. DÉFINITION DES PAGES
home = st.Page("1_🏠_Accueil.py", title="Accueil", icon="🏠")
codecarbon = st.Page("pages/2_⚙️_CodeCarbon.py", title="CodeCarbon", icon="⚙️")
promptcarbon = st.Page("pages/3_🍃_PromptCarbon.py", title="PromptCarbon", icon="🍃")

# 5. NAVIGATION (CACHÉE)
pg = st.navigation(
    {"Navigation": [home, codecarbon, promptcarbon]},
    position="hidden"
)

# 6. NAVBAR
col_logo, col_btn1, col_btn2, col_btn3 = st.columns([5, 1, 1, 1], gap="large", vertical_alignment="center")

with col_logo:
    st.markdown('<span class="nav-logo">🌐 TelecomCarbon</span>', unsafe_allow_html=True)

with col_btn1:
    st.page_link(home, label="Accueil", icon="🏠")

with col_btn2:
    st.page_link(codecarbon, label="CodeCarbon", icon="⚙️")

with col_btn3:
    st.page_link(promptcarbon, label="PromptCarbon", icon="🍃")

# 7. LANCEMENT
pg.run()