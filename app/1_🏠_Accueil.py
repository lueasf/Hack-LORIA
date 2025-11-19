# Accueil.py
import streamlit as st
import base64
import os
import plotly.graph_objects as go
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.map import create_carbon_intensity_map

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
    </style>
    """, unsafe_allow_html=True)

# Centrer le titre
st.markdown("<h1 style='text-align: center;'>Bienvenue sur TelecomCarbon ! 🌿</h1>", unsafe_allow_html=True)

# st.markdown("Choississez une application ci-dessous.")

# Créer des colonnes pour centrer les boutons
col_spacer1, col1, col2, col_spacer2 = st.columns([1, 2, 2, 1])

with col1:
    st.subheader("🍃 PromptCarbon")
    st.write("Mesurez l'empreinte carbone de vos prompts.")
    if st.button("Aller au comparateur"):
        # Cette fonction change de page programmatiquement
        st.switch_page("pages/3_🍃_PromptCarbon.py")

with col2:
    st.subheader("🌍 CodeCarbon")
    st.write("Mesurez l'empreinte carbone de vos scripts.")
    if st.button("Lancer le calculateur"):
        st.switch_page("pages/2_🌍_CodeCarbon.py")

# Ajouter une citation centrée dans un encadré transparent
st.markdown("""
<div style="
    background: rgba(255, 255, 255, 0.25);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin: 10rem auto;
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
""", unsafe_allow_html=True)

st.sidebar.success("Sélectionnez une page ci-dessus.")

# Ajouter un espacement pour permettre le scroll avant le graphique
st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)

# Ajouter un graphique interactif Plotly
st.markdown("---")
st.markdown("### Impact environnemental du numérique")

# Données d'exemple pour le graphique
fig = go.Figure()

# Données d'exemple : émissions CO2 par activité numérique (en g CO2)
activities = ['Streaming 1h', 'Requête web', 'Email simple', 'Email avec PJ', 'Visio 1h']
emissions = [36, 0.2, 4, 50, 150]

fig.add_trace(go.Bar(
    x=activities,
    y=emissions,
    marker=dict(
        color=emissions,
        colorscale='Greens',
        showscale=True,
        colorbar=dict(title="g CO2")
    ),
    text=[f"{e} g" for e in emissions],
    textposition='auto',
))

fig.update_layout(
    title="Empreinte carbone d'activités numériques courantes",
    xaxis_title="Activité",
    yaxis_title="Emissions CO2 (grammes)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(255,255,255,0.3)',
    font=dict(color='#000000', family='Righteous'),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

# Ajouter un espacement
st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)

# Ajouter la carte du mix énergétique
st.markdown("### Mix Énergétique Mondial")

fig_map = create_carbon_intensity_map()
st.plotly_chart(fig_map, use_container_width=True)

# Ajouter un espacement pour permettre le scroll
st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)

# Ajouter un footer beige
st.markdown("""
<div class="custom-footer">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="margin: 1rem;">
            <h3 style="color: #000000; margin-bottom: 1rem; font-weight: 700;">Contact</h3>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:antoine.bretzner@telecomnancy.eu" style="color: #333333; text-decoration: none;">antoine.bretzner@telecomnancy.eu</a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:chloe.wiatt@telecomnancy.eu" style="color: #333333; text-decoration: none;">chloe.wiatt@telecomnancy.eu</a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="mailto:lucie.correia@telecomnancy.eu" style="color: #333333; text-decoration: none;">lucie.correia@telecomnancy.eu</a></p>
            </div>
        <div style="margin: 1rem;">
            <h3 style="color: #000000; margin-bottom: 1rem; font-weight: 700;">À propos</h3>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://telecomnancy.univ-lorraine.fr/" target="_blank" style="color: #333333; text-decoration: none;"><u>Telecom Nancy</u></a></p>
            <p style="color: #333333; margin: 0.5rem 0;"><a href="https://www.loria.fr/fr/" target="_blank" style="color: #333333; text-decoration: none;"><u>LORIA</u></a></p>
        </div>
        <div style="margin: 1rem;">
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