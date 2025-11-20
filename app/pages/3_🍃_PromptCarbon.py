import sys
import os
import base64 # Ajout de l'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
from pathlib import Path
from backend.config import MODELS_LIST
from backend.llm_caller import call_llm
from backend.utils import load_json, save_json
from backend.compute_LLM_footprint import compute_carbon
from app.page_llm_calcul import show_calculation


# -----------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------
st.set_page_config(
    page_title="LLM Comparison & Carbon Tracking",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# FICHIERS JSON
# -----------------------------
PROMPTS_FILE = Path("data/prompts.json")
SESSION_FILE = Path("data/session_data.json")

if "app_started" not in st.session_state:
    save_json(SESSION_FILE, [])
    save_json(PROMPTS_FILE, [])
    
    st.session_state.app_started = True

PROMPTS_FILE.parent.mkdir(parents=True, exist_ok=True)

if not PROMPTS_FILE.exists():
    PROMPTS_FILE.write_text("[]")

if not SESSION_FILE.exists():
    SESSION_FILE.write_text("[]")

# -----------------------------
# INITIALISATION SESSION STATE
# -----------------------------
if "prompt_validated" not in st.session_state:
    st.session_state.prompt_validated = False

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

if "selected_provider" not in st.session_state:
    st.session_state.selected_provider = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "last_tdev" not in st.session_state:
    # dernier temps de développement (s) mesuré entre envoi et réception
    st.session_state.last_tdev = 0.0

# --- DÉBUT BLOC STYLE ACCUEIL ---
css_path = "app/accueil_styles.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        css_content = f.read()
    
    st.markdown(f"""
        <style>
            {css_content}
            .stApp {{
                /* Dégradé du vert clair vers un vert plus soutenu */
                background: linear-gradient(135deg, #94a773 0%, #94a45a 100%);
                background-attachment: fixed;
            }}
            /* Style pour les items de comparaison */
            .comparison-item {{
                background: rgba(255, 255, 255, 0.6);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }}
            
            /* --- NOUVEAU : Style pour les expanders (menus déroulants) en blanc --- */
            [data-testid="stExpander"] {{
                background-color: #ffffff !important;
                border-radius: 8px !important;
                border: none !important;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                color: #000000 !important;
            }}
            [data-testid="stExpander"] summary {{
                color: #000000 !important;
            }}
            [data-testid="stExpander"] summary:hover {{
                color: #333333 !important;
            }}
            /* Force la couleur du texte à l'intérieur en noir */
            [data-testid="stExpander"] p, [data-testid="stExpander"] li, [data-testid="stExpander"] span, [data-testid="stExpander"] div {{
                color: #000000 !important;
            }}

            /* --- CORRECTION : Mise en valeur des chiffres (Metrics) --- */
            
            /* 1. Forcer la couleur BLANCHE partout (Sidebar + Main) */
            [data-testid="stMetricValue"], [data-testid="stMetricValue"] > div, [data-testid="stMetricValue"] * {{
                color: #ffffff !important;
            }}
            
            [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] > div, [data-testid="stMetricLabel"] * {{
                color: #f0f0f0 !important; /* Blanc cassé pour les titres */
            }}

            /* 2. Taille GÉANTE uniquement pour la zone principale */
            section.main [data-testid="stMetricValue"] > div {{
                font-size: 3.5rem !important; /* Encore plus gros pour bien voir */
                font-weight: 800 !important;
                text-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            
            section.main [data-testid="stMetricLabel"] > div {{
                font-size: 1.2rem !important;
            }}

            /* 3. Taille NORMALE pour la sidebar (pour ne pas casser l'affichage) */
            [data-testid="stSidebar"] [data-testid="stMetricValue"] > div {{
                font-size: 1.8rem !important; /* Taille raisonnable */
                text-shadow: none;
            }}
        </style>
    """, unsafe_allow_html=True)

st.markdown("""<div style="
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
    padding: 0 2rem;
    z-index: 999998;
">
    <div style="margin-left: 2rem; font-size: 1.5rem; font-weight: 700; color: #000000; font-family: 'Righteous', sans-serif;">
        TelecomCarbon 🌿
    </div>
</div>
<div style='margin-top: 3rem;'></div>
""", unsafe_allow_html=True)
# --- FIN BLOC STYLE ACCUEIL ---

# On supprime l'ancien load_css
# load_css(os.path.join(os.path.dirname(__file__), "styles.css"))

# Statistiques globales dans la sidebar

# On crée un emplacement vide dans la sidebar
sidebar_placeholder = st.sidebar.empty()

# On définit une fonction qui sait lire le JSON et remplir cet emplacement
def update_sidebar_stats():
    current_data = load_json(SESSION_FILE)
    
    # On "entre" dans le placeholder pour écrire dedans
    with sidebar_placeholder.container():
        st.write("") # Petit espacement

        if current_data:
            # 1. Calculs des données brutes
            total_calls = len(current_data)
            total_carbon = sum(entry['carbon'] for entry in current_data)
            avg_carbon = total_carbon / total_calls
            avg_time = sum(entry['tdev_seconds'] for entry in current_data) / total_calls

            st.markdown("### Statistiques de la session")
            st.metric("Appels totaux", total_calls)
            st.metric("Émissions totales", f"{total_carbon:.4f} gCO₂e") # Précision augmentée
            st.metric("Moyenne par appel", f"{avg_carbon:.4f} gCO₂e")
            st.metric("Temps moyen", f"{avg_time:.2f} s")

            FACTOR_LED_G_PER_H = 1.3   # ~1.3 g par heure pour une LED 10W (mix moyen)
            FACTOR_CAR_G_PER_M = 0.12  # ~120 g/km soit 0.12 g/m pour une voiture

            equiv_led_hours = total_carbon / FACTOR_LED_G_PER_H
            equiv_car_meters = total_carbon / FACTOR_CAR_G_PER_M

            st.markdown("### Équivalences")
            
            # Affichage dynamique
            st.metric(
                "💡 Ampoule LED (10W)", 
                f"{equiv_led_hours:.2f} h", 
                help="Temps d'éclairage équivalent (Facteur: 1.3g/h)"
            )
            
            st.metric(
                "🚗 Voiture thermique", 
                f"{equiv_car_meters:.2f} m", 
                help="Distance parcourue équivalente (Facteur: 0.12g/m)"
            )
        else:
            st.caption("Aucune donnée de session.")



# On appelle la fonction une première fois pour afficher l'état actuel (avant calcul)
update_sidebar_stats()

# -----------------------------
# CALLBACKS
# -----------------------------
def validate_prompt():
    if st.session_state.current_prompt.strip() != "":
        st.session_state.prompt_validated = True
        
        # Sauvegarde dans prompts.json
        prompts = load_json(PROMPTS_FILE)
        prompts.append({"prompt": st.session_state.current_prompt})
        save_json(PROMPTS_FILE, prompts)

def new_prompt():
    st.session_state.prompt_validated = False
    st.session_state.current_prompt = ""
    st.session_state.current_response = ""
    st.session_state.selected_model = None

    try:
        save_json(PROMPTS_FILE, [])
        save_json(SESSION_FILE, [])
        st.info("Historique des prompts et de la session vidé.")
    except Exception as e:
        st.error(f"Impossible de vider le fichier des prompts : {e}")

def save_session_entry(prompt, model_name, response, carbon, tdev_seconds):
    """Enregistre une entrée de session incluant le temps de réponse (tdev en secondes)."""
    session_data = load_json(SESSION_FILE)
    session_data.append({
        "prompt": prompt,
        "model": model_name,
        "response": response,
        "carbon": carbon,
        "tdev_seconds": tdev_seconds,
    })
    save_json(SESSION_FILE, session_data)


# -----------------------------
# PAGE FRONT
# -----------------------------
st.title("📄 Session LLM - Évaluation de l'empreinte carbone")

st.write("Cette page vous permet d’envoyer un prompt à plusieurs modèles LLM, "
         "d’enregistrer chaque résultat, et de suivre l’empreinte carbone associée.")


# -------------------------------------------------
# 1. ÉCRITURE DU PROMPT + VALIDATION
# -------------------------------------------------
st.subheader("1. Prompt")

if not st.session_state.prompt_validated:
    st.session_state.current_prompt = st.text_area(
        "Écrivez ou collez votre prompt :",
        value=st.session_state.current_prompt,
        height=150,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Valider le prompt", on_click=validate_prompt)

    with col2:
        st.button("Nouveau prompt", on_click=new_prompt)

else:
    st.success("Prompt validé 🔒 — pas modifiable.")
    st.write(f"**Prompt :** {st.session_state.current_prompt}")
    st.button("Nouveau prompt", on_click=new_prompt)


# Si le prompt n'est pas validé, on empêche la suite
if not st.session_state.prompt_validated:
    st.stop()


# -------------------------------------------------
# 2. SÉLECTION DU MODÈLE
# -------------------------------------------------
st.subheader("2. Choix du provider et du modèle LLM")

# Choix du provider
st.session_state.selected_provider = st.selectbox(
    "Choisissez un provider :", 
    list(MODELS_LIST.keys()),
    index=None,
    placeholder="Sélectionnez un provider"
)

if st.session_state.selected_provider is None:
    st.stop()

provider = st.session_state.selected_provider
models_for_provider = MODELS_LIST.get(provider, [])

if not models_for_provider:
    st.warning(f"Aucun modèle disponible pour le provider {provider}.")
    st.stop()

st.session_state.selected_model = st.selectbox(
    "Choisissez un modèle spécifique :", 
    models_for_provider,
    index=None,
    placeholder="Sélectionnez un modèle LLM"
)

if st.session_state.selected_model is None:
    st.stop()


# -------------------------------------------------
# 3. APPEL LLM + AFFICHAGE RÉPONSE
# -------------------------------------------------
st.subheader("3. Réponse du modèle")

if st.button("Envoyer le prompt au modèle"):
    with st.spinner("Le modèle réfléchit..."):
        
        response, tdev = call_llm(
            st.session_state.selected_provider,
            st.session_state.current_prompt,
            model=st.session_state.selected_model,
        )
        
        # On sauvegarde la réponse (qu'il s'agisse d'un succès ou d'une erreur)
        st.session_state.current_response = response
        st.session_state.last_tdev = tdev

        # Indique quel modèle a produit cette réponse et marque la réponse comme "à sauvegarder"
        st.session_state.response_model = st.session_state.selected_model
        st.session_state.pending_save = True

# Cette partie gère l'affichage de la réponse ou de l'erreur stockée en session
if st.session_state.current_response:
    response_data = st.session_state.current_response

    # Vérifie si la réponse est un dictionnaire et si elle contient une clé 'error'
    if isinstance(response_data, dict) and 'error' in response_data:
        st.error(f"**Une erreur est survenue lors de l'appel au modèle :**\n\n{response_data['error']}")
    
    # Sinon, si la réponse est bien une chaîne de caractères (cas du succès)
    elif isinstance(response_data, str):
        st.markdown("**Réponse du modèle :**")
        st.markdown(f"```\n{response_data}\n```")
        
    # Cas de sécurité si la réponse n'est ni un dictionnaire d'erreur, ni une string
    else:
        st.warning("La réponse reçue est dans un format inattendu.")
        st.write(response_data)


# -------------------------------------------------
# 4. EMPREINTE CARBONE
# -------------------------------------------------
if st.session_state.current_response:
    st.subheader("4. Empreinte carbone estimée")

    # Utiliser explicitement le modèle qui a produit la réponse (s'il existe)
    model_for_response = st.session_state.get("response_model", st.session_state.selected_model)

    carbon = compute_carbon(
        model_for_response,
        st.session_state.current_prompt,
        st.session_state.current_response,
        st.session_state.last_tdev,
    )

    st.metric(label="Empreinte carbone (g CO₂e)", value=f"{carbon:.4f}")

    # Affichage du temps de réponse
    st.metric(label="Temps de réponse (s)", value=f"{st.session_state.last_tdev:.3f}")

    # Sauvegarde uniquement si la réponse vient d'être récupérée et n'a pas encore été sauvegardée
    if st.session_state.get("pending_save", False):
        # protège contre l'enregistrement si l'utilisateur a changé de modèle entre-temps
        if st.session_state.get("response_model") == model_for_response:
            save_session_entry(
                st.session_state.current_prompt,
                model_for_response,
                st.session_state.current_response,
                carbon,
                st.session_state.last_tdev,
            )
            # Met à jour les stats dans la sidebar
            update_sidebar_stats()

        # réinitialiser le marqueur pour éviter de resauvegarder lors des reruns
        st.session_state.pending_save = False

    # Importation locale (lazy import) : 
    # Le module n'est importé que lorsque Python lit cette ligne, pas au démarrage du script.
    def afficher_details():
        show_calculation()

    # Le composant natif pour afficher/masquer
    with st.expander("Voir l'explication détaillée"):
        afficher_details()

# -------------------------------------------------
# 5. Visualisation de session
# -------------------------------------------------
st.subheader("5. Visualisation comparative des modèles")

# Import du module de visualisation
from backend.visualisation import create_model_comparison_chart, create_session_timeline

# Créer et afficher le graphique comparatif
fig_comparison = create_model_comparison_chart()
st.plotly_chart(fig_comparison, use_container_width=True)

# Afficher également la timeline (optionnel)
with st.expander("📊 Voir la chronologie de la session"):
    fig_timeline = create_session_timeline()
    st.plotly_chart(fig_timeline, use_container_width=True)

# -------------------------------------------------
# 6. Historique de la session
# -------------------------------------------------

st.subheader("6. Historique des appels LLM de la session")

session_data = load_json(SESSION_FILE)
if not session_data:
    st.info("Aucun appel LLM enregistré dans cette session.")
else:
    for i, entry in enumerate(session_data):
        # On utilise flex et gap pour l'espacement, et un style de badge pour chaque métrique
        # Note : Ici on met les chiffres en vert foncé car le fond de la carte est clair
        st.markdown(f"""
            <div class="comparison-item" style="padding: 15px; border-radius: 10px; background-color: rgba(255, 255, 255, 0.85); margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.2em; display: block; margin-bottom: 12px; color: #1a4a15;">Modèle : {entry['model']}</strong>
                <div style="display: flex; flex-wrap: wrap; gap: 25px; align-items: center;">
                    <span style="background: #e8f5e9; padding: 5px 10px; border-radius: 8px; border: 1px solid #c8e6c9;">
                        ⏳ <b style="color: #2e7d32; font-size: 1.2em;">{entry['tdev_seconds']:.2f}</b> <span style="color: #555">s</span>
                    </span>
                    <span style="background: #e8f5e9; padding: 5px 10px; border-radius: 8px; border: 1px solid #c8e6c9;">
                        🌳 <b style="color: #1b5e20; font-size: 1.4em;">{entry['carbon']:.4f}</b> <span style="color: #555">gCO₂e</span>
                    </span>
                    <span style="color: #666;">
                        💬 <b>{len(entry['response'].split())}</b> mots
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
