import streamlit as st
import json
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


def compute_carbon(model_name, prompt, response):
    """
    Stub pour calculer l'empreinte carbone.
    Remplace par ta vraie fonction.
    """
    # Ex : carbon.compute(model_name, len(prompt), len(response))
    return 0.123  # placeholder


def save_session_entry(prompt, model_name, response, carbon):
    session_data = load_json(SESSION_FILE)
    session_data.append({
        "prompt": prompt,
        "model": model_name,
        "response": response,
        "carbon": carbon
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
    "openai/gpt-4.1",
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
    response = call_llm_api(
        st.session_state.current_prompt, 
        st.session_state.selected_model
    )
    st.session_state.current_response = response

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
    )

    st.metric(label="Empreinte carbone (kg CO₂e)", value=f"{carbon:.4f}")

    # Sauvegarde
    save_session_entry(
        st.session_state.current_prompt,
        st.session_state.selected_model,
        st.session_state.current_response,
        carbon
    )


# -------------------------------------------------
# 5. Visualisation de session (placeholder)
# -------------------------------------------------
st.subheader("5. Visualisation de la session (à venir)")
st.info("La partie visualisation sera ajoutée plus tard (graphiques, stats, etc.).")
