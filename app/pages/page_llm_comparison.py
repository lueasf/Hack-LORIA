import streamlit as st
import json
import time
from pathlib import Path

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
# FONCTIONS UTILITAIRES
# -----------------------------
def load_json(path):
    try:
        return json.loads(path.read_text())
    except:
        return []

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


# -----------------------------
# INITIALISATION SESSION STATE
# -----------------------------
if "prompt_validated" not in st.session_state:
    st.session_state.prompt_validated = False

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

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


def call_llm_api(prompt, model_name):
    """
    Stub provisoire à remplacer par ton appel API :
    """
    # Ex : appeler Groq, OpenAI, ou autre
    # return llm_api.call(prompt, model_name)
    return f"[FAKE RESPONSE from {model_name}] for prompt: {prompt}"


def compute_carbon(model_name, prompt, response, tdev):
    """
    Stub pour calculer l'empreinte carbone.
    Remplace par ta vraie fonction.
    """
    # Assumptions :
    hardware_profiles = {
        "openai/gpt-3.5": {
            "device_count": 2,     
            "device_power_kw": 0.6,
            "chip_type": "H100"
        },
    }

    # Si modèle inconnu
    profile = hardware_profiles.get(model_name, {
        "device_count": 1, "device_power_kw": 0.5, "chip_type": "H100"
    })

    P = profile["device_count"] * profile["device_power_kw"]  # Puissance totale (kW)
    PUE = 1.1
    Ci = {"us": 0.4, "fr": 0.06} # kg CO2e/kWh

    tdev_h = tdev / 3600  # conversion secondes -> heures

    # Calcul de l'empreinte carbone
    operational_carbon = P * PUE * Ci["us"] * tdev_h

    # C02 de fabrication du matériel (valeur du papier)
    cpu = 1.47 # kg
    DRAM = 102.4 # kg
    SSD = 576 # kg
    H100 = 14.652 # kg
    total_hardware_co2 = cpu + DRAM + SSD + H100

    LT = 4 * 365.25 * 24 # Durée de vie du matériel en heures

    hardware_carbon = (tdev_h / LT) * total_hardware_co2

    total_carbon = (operational_carbon + hardware_carbon) * 1000 # Conversion en grammes

    return total_carbon


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
st.subheader("2. Sélection du modèle LLM")

model_list = [
    "groq/llama3-8b",
    "groq/mixtral-8x7b",
    "openai/gpt-4.1-mini",
    "openai/gpt-3.5",
]

st.session_state.selected_model = st.selectbox(
    "Choisissez un modèle :", 
    model_list,
    index=None,
    placeholder="Sélectionnez un modèle"
)

if st.session_state.selected_model is None:
    st.stop()


# -------------------------------------------------
# 3. APPEL LLM + AFFICHAGE RÉPONSE
# -------------------------------------------------
st.subheader("3. Réponse du modèle")

if st.button("Envoyer le prompt au modèle"):
    # Mesure du temps écoulé entre l'envoi et la réception (tdev)
    start = time.time()
    response = call_llm_api(
        st.session_state.current_prompt,
        st.session_state.selected_model,
    )
    tdev = time.time() - start
    st.session_state.current_response = response
    st.session_state.last_tdev = tdev

if st.session_state.current_response:
    st.write("### Réponse :")
    st.write(st.session_state.current_response)


# -------------------------------------------------
# 4. EMPREINTE CARBONE
# -------------------------------------------------
if st.session_state.current_response:
    st.subheader("4. Empreinte carbone estimée")

    carbon = compute_carbon(
        st.session_state.selected_model,
        st.session_state.current_prompt,
        st.session_state.current_response,
        st.session_state.last_tdev,
    )

    st.metric(label="Empreinte carbone (g CO₂e)", value=f"{carbon:.4f}")

    # Affichage du temps de réponse
    st.metric(label="Temps de réponse (s)", value=f"{st.session_state.last_tdev:.3f}")

    # Sauvegarde (inclut tdev)
    save_session_entry(
        st.session_state.current_prompt,
        st.session_state.selected_model,
        st.session_state.current_response,
        carbon,
        st.session_state.last_tdev,
    )


# -------------------------------------------------
# 5. Visualisation de session (placeholder)
# -------------------------------------------------
st.subheader("5. Visualisation de la session (à venir)")
st.info("La partie visualisation sera ajoutée plus tard (graphiques, stats, etc.).")
