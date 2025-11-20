# Accueil.py
import streamlit as st
import base64
import os
import plotly.graph_objects as go
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.plot import create_carbon_intensity_map, create_lightbulb_chart, create_numeric_activity

st.set_page_config(
    page_title="Accueil",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger l'image en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Charger l'image de fond
img_path = "app/assets/fond6.png"
if os.path.exists(img_path):
    img_base64 = get_base64_image(img_path)
    
    # Charger le CSS externe
    css_path = "app/accueil_styles.css"
    with open(css_path) as f:
        css_content = f.read()
    
    # Appliquer le CSS avec l'image de fond
    # Appliquer le CSS avec l'image de fond
    st.markdown(f"""
        <style>
            {css_content}
            
            .stApp {{
                background-image: url("data:image/png;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Centrer les boutons (Fix précédent) */
            div.stButton {{
                display: flex;
                justify-content: center;
            }}
            
            /* Style de la flèche de scroll */
            .scroll-down {{
                text-align: center;
                margin-top: 2rem;
                cursor: pointer;
                animation: bounce 2s infinite;
            }}
            
            .scroll-down a {{
                text-decoration: none;
                color: #000000;
                font-size: 2rem;
                font-weight: bold;

                /* STYLE APPLE LIQUID (Glassmorphism) */
                background: rgba(255, 255, 255, 0.25); /* Transparent mais visible */
                backdrop-filter: blur(15px);           /* Le flou d'arrière-plan */
                border: 1px solid rgba(255, 255, 255, 0.3); /* Bordure subtile */
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Ombre douce */

                /* Forme ronde */
                width: 60px;
                height: 60px;
                border-radius: 50%;

                /* Centrage et AJUSTEMENT VERTICAL */
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding-top: 12px; /* <-- J'ai augmenté cette valeur pour descendre la flèche */
                transition: all 0.3s ease; /* Animation fluide au survol */
            }}

            /* Petit bonus : effet au survol */
            .scroll-down a:hover {{
                background: rgba(255, 255, 255, 0.4);
                transform: scale(1.1);
            }}

            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
                40% {{transform: translateY(-10px);}}
                60% {{transform: translateY(-5px);}}
            }}

            /* Style pour le conteneur des outils (Effet verre) */
            .tools-container {{
                background: rgba(255, 255, 255, 0.85); /* Fond blanc très opaque */
                border-radius: 20px;
                padding: 3rem 2rem;
                margin-top: 2rem;
                margin-bottom: 4rem;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }}
            
            .tool-title {{
                color: #2E7D32; /* Vert forêt pour le titre */
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
        </style>
    """, unsafe_allow_html=True)

# Barre de navigation en haut
st.markdown("""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 999998;
">
    <div style="margin-left: 2rem; font-size: 1.5rem; font-weight: 700; color: #000000; font-family: 'Righteous', sans-serif;">
        TelecomCarbon 🌿
    </div>
    <div style="display: flex; gap: 2rem; align-items: center;">
        <a href="#contact" style="color: #000000; text-decoration: none; font-weight: 500; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">Contact</a>
        <a href="#about" style="color: #000000; text-decoration: none; font-weight: 500; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">À propos</a>
        <a href="#links" style="color: #000000; text-decoration: none; font-weight: 500; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">Liens utiles</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Centrer le titre avec marge négative pour compenser la navbar
st.markdown("<div style='margin-top: -1rem;'><h1 style='text-align: center; font-size: 4rem'>Mesurez. Comprenez. Réduisez.</h1></div>", unsafe_allow_html=True)

# st.markdown("Choississez une application ci-dessous.")

# Ajouter une citation centrée dans un encadré transparent
# Ajouter une citation centrée + LA FLÈCHE
st.markdown("""
<div style="
    background: rgba(255, 255, 255, 0.25);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin: 3rem auto 1rem auto; /* Marge du bas réduite pour la flèche */
    max-width: 800px;
">
    <p style="font-size: 1.2rem; font-style: italic; color: #000000; margin: 0;">
        "L'intelligence artificielle est la nouvelle électricité, mais comme toute source d'énergie, 
        elle a un coût environnemental qu'il nous appartient de mesurer et de réduire."
    </p>
    <p style="color: #666666; margin-top: 1rem; font-size: 0.9rem;">
        — Notre engagement pour un numérique responsable
    </p>
</div>

<!-- La Flèche qui pointe vers l'ancre #nos-outils -->
<div class="scroll-down">
    <a href="#nos-outils">﹀</a>
</div>
""", unsafe_allow_html=True)

# Espacement pour laisser la flèche respirer
st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)

# --- DÉBUT DE LA SECTION OUTILS ---

# Ancre invisible pour le lien de la flèche
st.markdown("<div id='nos-outils' style='position: relative; top: -50px; visibility: hidden;'></div>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; margin-bottom: 2rem; color: #000;'>Nos solutions de mesure</h2>", unsafe_allow_html=True)

# Créer des colonnes pour centrer les boutons
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 class='tool-title' style='text-align: center;'>🍃 PromptCarbon</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 1.5rem;'>Estimez l'empreinte carbone générée par vos requêtes LLM.</p>", unsafe_allow_html=True)
    if st.button("Aller au comparateur", use_container_width=True):
        st.switch_page("pages/3_🍃_PromptCarbon.py")

with col2:
    st.markdown("<h3 class='tool-title' style='text-align: center;'>🌍 CodeCarbon</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 1.5rem;'>Intégrez le tracking carbone directement dans vos scripts Python.</p>", unsafe_allow_html=True)
    if st.button("Lancer le calculateur", use_container_width=True):
        st.switch_page("pages/2_⚙️_CodeCarbon.py")

# On ferme le conteneur visuel
st.markdown('</div>', unsafe_allow_html=True)


# Ajouter un espacement pour permettre le scroll avant le graphique
st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)


st.markdown("---")

st.markdown("### Impact environnemental du numérique")
fig_numeric_activity = create_numeric_activity()
st.plotly_chart(fig_numeric_activity, use_container_width=True)


st.markdown("### Impact environnemental de l'entraînement des LLMs")
fig_lightbulb = create_lightbulb_chart()
st.plotly_chart(fig_lightbulb, use_container_width=True)

# Ajouter un espacement

# Ajouter la carte du mix énergétique
st.markdown("### Mix Énergétique Mondial")

fig_map = create_carbon_intensity_map()
st.plotly_chart(fig_map, use_container_width=True)

# Ajouter un espacement pour permettre le scroll
st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)

# Ajouter un footer beige
st.markdown("""
<div class="custom-footer" id="contact">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="margin: 1rem;">
            <h3 style="color: #000000; margin-bottom: 1rem; font-weight: 700;">Contact</h3>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:antoine.bretzner@telecomnancy.eu" style="color: #333333; text-decoration: none;">antoine.bretzner@telecomnancy.eu</a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:chloe.wiatt@telecomnancy.eu" style="color: #333333; text-decoration: none;">chloe.wiatt@telecomnancy.eu</a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:lucie.correia@telecomnancy.eu" style="color: #333333; text-decoration: none;">lucie.correia@telecomnancy.eu</a></p>
            </div>
        <div style="margin: 1rem;" id="about">
            <h3 style="color: #000000; margin-bottom: 1rem; font-weight: 700;">À propos</h3>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://telecomnancy.univ-lorraine.fr/" target="_blank" style="color: #333333; text-decoration: none;"><u>Telecom Nancy</u></a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://www.loria.fr/fr/" target="_blank" style="color: #333333; text-decoration: none;"><u>LORIA</u></a></p>
        </div>
        <div style="margin: 1rem;" id="links">
            <h3 style="color: #000000; margin-bottom: 1rem; font-weight: 700;">Liens utiles</h3>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://codecarbon.io/" target="_blank" style="color: #333333; text-decoration: none;"><u>CodeCarbon Documentation</u></a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://arxiv.org/pdf/2309.14393" target="_blank" style="color: #333333; text-decoration: none;"><u>LLMCarbon Paper</u></a></p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(0, 0, 0, 0.1);">
        <p style="color: #666666;">© 2025 Telecom Nancy. Tous droits réservés.</p>
    </div>
</div>
""", unsafe_allow_html=True)