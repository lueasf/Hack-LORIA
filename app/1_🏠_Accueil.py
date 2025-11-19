import streamlit as st
import base64
import os
import plotly.graph_objects as go

# --- GESTION DU FOND D'ÉCRAN ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_path = "app/assets/fond6.png"
if os.path.exists(img_path):
    img_base64 = get_base64_image(img_path)
    
    # --- BLOC CSS & HTML ---

    st.markdown(f"""
    <style>
        /* Fond d'écran */
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Titre Principal */
        .main-title {{
            font-family: 'Inter', sans-serif;
            font-size: 5rem;
            font-weight: 800;
            text-align: center;
            margin-top: 2rem;
            text-shadow: 0 4px 30px rgba(0,0,0,0.8);
            margin-bottom: 0;
        }}
        
        /* Sous-titre */
        .subtitle {{
            font-size: 1.5rem;
            font-weight: 300;
            text-align: center;
            color: #e0e0e0 !important;
            margin-bottom: 4rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        }}

    </style>

    <!-- STRUCTURE HTML -->
    <div>
        <h1 style="font-size: 4rem; margin-bottom: 1rem; text-align:center">Mesurez. Comprenez. Réduisez.</h1>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
    <div style="
        display: block;
        background-color: rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 0.5rem;
        font-size: 2rem; 
        font-weight: 300;
        color: #ffffff;
        text-align: center;
        backdrop-filter: blur(4px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        width: 100%;
        margin-top: 2rem;
        margin-bottom: 30vh;
    ">
        « Le numérique n'est pas immatériel. C'est une industrie lourde, faite de métaux,
        d'énergie et d'infrastructures. Comprendre son impact est le premier pas vers
        une technologie durable. »
    </div>
""", unsafe_allow_html=True)


# --- 2. BOUTONS D'ACTION ---
st.markdown("<br>", unsafe_allow_html=True) # Petit espace

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("🍃 PromptCarbon")
    st.markdown("Mesurez l'empreinte carbone de vos prompts.")
    if st.button("Aller au comparateur", use_container_width=True):
        st.switch_page("pages/3_🍃_PromptCarbon.py")

with col2:
    st.subheader("🌍 CodeCarbon")
    st.markdown("Mesurez l'empreinte carbone de vos scripts.")
    if st.button("Lancer le calculateur", use_container_width=True):
        st.switch_page("pages/2_🌍_CodeCarbon.py")

# --- 3. GRAPHIQUE (CORRIGÉ) ---
st.markdown("---")
st.markdown("### 📊 Impact environnemental du numérique")

fig = go.Figure()
activities = ['Streaming 1h', 'Requête web', 'Email simple', 'Email avec PJ', 'Visio 1h']
emissions = [36, 0.2, 4, 50, 150]

fig.add_trace(go.Bar(
    x=activities,
    y=emissions,
    marker=dict(
        color=emissions,
        colorscale='Greens',
        showscale=True,
        # --- CORRECTION ICI ---
        colorbar=dict(
            # Le titre est maintenant un dictionnaire contenant text et font
            title=dict(text="g CO2", font=dict(color='white')),
            tickfont=dict(color='white')
        )
    ),
    text=[f"{e} g" for e in emissions],
    textposition='auto',
    textfont=dict(color='white')
))

fig.update_layout(
    title=dict(text="Empreinte carbone d'activités numériques courantes", font=dict(color='white', size=20)),
    xaxis=dict(title="Activité", color='white', tickfont=dict(color='white')),
    yaxis=dict(title="Emissions CO2 (grammes)", color='white', tickfont=dict(color='white')),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(20, 20, 20, 0.6)',
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

# Espace vide pour le scroll
st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)

# --- 4. FOOTER ---
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