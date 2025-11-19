import sys
import os
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
st.title("📄 Session LLM — Évaluation de l'empreinte carbone")

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
# 5. Visualisation de session (placeholder)
# -------------------------------------------------
st.subheader("5. Visualisation de la session (à venir)")
st.info("La partie visualisation sera ajoutée plus tard (graphiques, stats, etc.).")
