# Accueil.py
import streamlit as st
import base64
import os
import plotly.graph_objects as go
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.plot import create_carbon_intensity_map, create_lightbulb_chart, create_numeric_activity, create_adoption_chart, create_camenbert

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

st.markdown("""
    <div style="text-align: center; max-width: 1000px; margin: 0 auto 3rem auto;">
        <h2 style="color: #1a1a1a; margin-bottom: 1rem; font-size: 3rem;">Nos solutions de mesure</h2>
        <p style="text-align: justify; color: #4a4a4a; font-size: 1.2rem; line-height: 1.6;">
            Derrière la magie de l'IA et la rapidité de nos programmes se cachent des serveurs, des GPU et des kWh consommés.
            Il est temps d'intégrer la variable <b>Carbone</b> à vos critères de performance.<br><br>
            Ne codez plus à l'aveugle. Utilisez nos calculateurs dédiés pour auditer vos pratiques et rejoindre le mouvement du <i>Green Coding</i>.
        </p>
    </div>
""", unsafe_allow_html=True)

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



# --- FONCTION UTILITAIRE POUR AFFICHER UNE CARTE KPI ---
def display_kpi(value, label, subtext=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div style="font-size: 0.8rem; color: #888; margin-top: 5px;">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# Espacement
st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)

st.markdown("---")


# --- TITRE DE SECTION ---
st.markdown("<div class='section-header'>Panorama de l'Impact Numérique</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 3rem; font-size: 1.1rem; color: #444;'>Comprendre l'échelle du problème est la première étape vers la solution.</p>", unsafe_allow_html=True)
# Autre choix possible pour le sous titre / texte
# st.markdown("""
#     <p style='text-align: center; margin-bottom: 3rem; font-size: 1.15rem; color: #4a4a4a; max-width: 900px; margin-left: auto; margin-right: auto; line-height: 1.6;'>
#         Bien que souvent perçu comme immatériel, le monde numérique repose sur une infrastructure physique colossale. 
#         Voici quelques chiffres pour visualiser l'invisible.
#     </p>
# """, unsafe_allow_html=True)


# --- LIGNE 1 : LES CHIFFRES CLÉS (4 colonnes) ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    display_kpi("4%", "Émissions Mondiales", "Plus que l'aviation civile")
with kpi2:
    display_kpi("+9%", "Croissance Annuelle", "De l'empreinte numérique")
with kpi3:
    display_kpi("10%", "Électricité Mondiale", "Consommée par le numérique")
with kpi4:
    display_kpi("400g", "Empreinte Smartphone", "De CO2 à la fabrication")

# Espacement
st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

# --- LIGNE 2 : Volume & Complexité ---
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("<h2 style='text-align: center;'>Déluge de données</h2>", unsafe_allow_html=True)
    # On utilise du Markdown simple avec couleur pour simuler une "Big Metric"
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <span style='font-size: 4.5rem; font-weight: 800; color: #1a1a1a;'>2.5 Mds</span><br>
            <span style='font-size: 1.5rem; color: #2E7D32; font-weight: bold;'>de prompts / jour</span>
            <p style='color: #666; margin-top: 10px;'>Générés uniquement sur ChatGPT.</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("<h2 style='text-align: center;'>Complexité de GPT-4</h2>", unsafe_allow_html=True)
    st.write("Comparaison en équivalent de neurones humains (21 cerveaux) :")
    
    # Astuce : On génère une chaine de caractères avec 21 cerveaux
    # C'est du texte pur, donc Streamlit l'affiche sans bug
    brains = "🧍‍♂️​ " * 21
    st.markdown(f"<div style='font-size: 2rem; line-height: 1.5; text-align: center; filter: brightness(0);'>{brains}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-style: italic;'>Un modèle massif pour des questions parfois futiles...</p>", unsafe_allow_html=True)

st.markdown("---")

# 1. Graphique d'Adoption (Pleine largeur pour bien lire les dates)
st.markdown("### 📈 Une croissance sans précédent")
st.markdown("<p style='color: #666; margin-bottom: 1rem;'>La demande explose, entraînant une augmentation mécanique de la consommation.</p>", unsafe_allow_html=True)
fig_adoption = create_adoption_chart()
st.plotly_chart(fig_adoption, use_container_width=True)

st.markdown("---")

# 2. Graphique Ampoules (Pleine largeur pour bien comparer)
st.markdown("### ⚡ Le coût énergétique de l'entraînement")
st.markdown("<p style='color: #666; margin-bottom: 1rem;'>Créer ces modèles demande une quantité d'énergie colossale, bien avant leur première utilisation.</p>", unsafe_allow_html=True)

fig_lightbulb = create_lightbulb_chart()
st.plotly_chart(fig_lightbulb, use_container_width=True)

# --- LIGNE 3 : La Politesse (Section dédiée) ---
st.markdown("### Le coût caché de la politesse")
st.markdown(
    "<p style='text-align: center; font-size: 1.1rem;'>125 millions de prompts par jour servent uniquement à dire 'Bonjour' ou 'Merci'.</p>", 
    unsafe_allow_html=True
)

# Le gros chiffre rouge au milieu
st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <span style='font-size: 4rem; font-weight: 800; color: #d32f2f;'>250 Tonnes CO2</span><br>
        <span style='font-size: 1.2rem; color: #d32f2f; font-weight: bold;'>Gaspillées chaque jour</span>
    </div>
""", unsafe_allow_html=True)

# Les 3 comparaisons en colonnes natives Streamlit
comp1, comp2, comp3 = st.columns(3)

with comp1:
    st.markdown("""
        <div style='text-align: center;'>
            <div style='font-size: 3rem; filter: grayscale(50%);'>🏎️</div>
            <div style='font-weight: bold; margin-top: 0.5rem;'>50x le tour de la Terre</div>
            <div class='grey-caption'>En voiture thermique</div>
        </div>
    """, unsafe_allow_html=True)

with comp2:
    st.markdown("""
        <div style='text-align: center;'>
            <div style='font-size: 3rem; filter: grayscale(50%);'>🥩</div>
            <div style='font-weight: bold; margin-top: 0.5rem;'>60 000 Steaks</div>
            <div class='grey-caption'>Jetés à la poubelle</div>
        </div>
    """, unsafe_allow_html=True)

with comp3:
    st.markdown("""
        <div style='text-align: center;'>
            <div style='font-size: 3rem; filter: grayscale(50%);'>🧊</div>
            <div style='font-weight: bold; margin-top: 0.5rem;'>3 Terrains de tennis</div>
            <div class='grey-caption'>De banquise fondus</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- LIGNE 4 : GRAPHIQUES CÔTE À CÔTE ---
col_graph1, col_graph2 = st.columns([1, 1]) # 50% / 50%

with col_graph1:
    st.markdown("### 📉 Activités courantes")
    fig_bar = create_numeric_activity()
    st.plotly_chart(fig_bar, use_container_width=True)

with col_graph2:
    st.markdown("### 📊 Parts d'utilisations des ChatBots")
    fig_pie = create_camenbert()
    st.plotly_chart(fig_pie, use_container_width=True)

# --- LIGNE 3 : LA CARTE ---
st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("### Intensité Carbone du Mix Électrique")
st.markdown("<p style='font-size: 0.9rem; color: #666;'>L'impact de votre code dépend de l'endroit où il s'exécute.</p>", unsafe_allow_html=True)

# Ta carte existante
fig_map = create_carbon_intensity_map()
# On s'assure que la carte a un fond transparent pour s'intégrer
fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo=dict(bgcolor='rgba(0,0,0,0)'))
st.plotly_chart(fig_map, use_container_width=True)

# --- FOOTER (Ton code existant) ---
# ci-dessous


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