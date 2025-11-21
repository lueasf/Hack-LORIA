# Hack-LORIA : TelecomCarbon 🌿

> **Mesurez l'impact CO₂ de votre code et de vos prompts.**

Ce projet a été développée à l'occasion d'un Hackathon pour la filière IAMD de Télécom Nancy. Il propose une interface Streamlit unifiée pour estimer l'empreinte carbone de deux usages courants en IA :

1.  **L'exécution locale** de scripts Python/Java (via `codecarbon`).
2.  **L'inférence LLM** via API (OpenAI, Gemini, Groq, HuggingFace).

L'objectif ? Rendre tangible le coût invisible du numérique, en combinant mesure réelle (énergie consommée) et estimation matérielle (coût de fabrication/embodied).

## ⚡ Quick Start

### 1\. Installation

```bash
# Cloner et préparer l'environnement
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

### 2\. Configuration (.env)

Créez un fichier `.env` à la racine. Remplissez uniquement les clés des providers que vous comptez utiliser.

```env
# API Keys (Laisser vide si inutilisé)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
GROQ_API_KEY=...
HUGGINGFACE_API_KEY=hf_...

# Modèles (Le premier de la liste est le défaut)
OPENAI_MODEL=gpt-4o,gpt-3.5-turbo
GEMINI_MODEL=gemini-1.5-flash
GROQ_MODEL=llama-3.3-70b-versatile
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

### 3\. Lancement

```bash
streamlit run app/1_🏠_Accueil.py
```


## 🛠 fonctionnalités

L'application est divisée en deux volets principaux accessibles via la sidebar Streamlit.

### 🐍 1. Analyse de Scripts (CodeCarbon)

Collez votre code Python ou uploadez un fichier `.py`. L'application l'exécute dans un environnement instrumenté.

  * **Métriques :** Durée, Énergie (kWh), Émissions (kgCO₂eq).
  * **Logs :** Capture de `stdout`/`stderr` en temps réel.
  * **Data :** Génération et téléchargement automatique d'un fichier `emissions.csv`.

### 🤖 2. Comparateur LLM

Envoyez un prompt à différents modèles et comparez leur empreinte estimée.

  * **Multi-Provider :** Supporte OpenAI, Google Gemini, Groq et Hugging Face Hub.
  * **Calcul Hybride :** Prend en compte la latence réseau (temps d'inférence) et le profil matériel théorique des serveurs.
  * **Gestion d'erreurs :** Gère les timeouts et les rate-limits proprement.


## 📐 Comment on calcule le CO₂ ? (Méthodologie)

C'est ici que ça devient intéressant. Pour les LLM, nous n'avons pas accès au compteur électrique d'OpenAI ou de Google. Nous utilisons une approche heuristique basée sur la littérature scientifique (notamment [arXiv:2309.14393](https://arxiv.org/pdf/2309.14393)).

L'empreinte totale est la somme de l'opérationnel (électricité) et du matériel (fabrication amortie) :

$$CO2_{total} = (CO2_{op} + CO2_{hw})$$

### 1\. Consommation Opérationnelle ($CO2_{op}$)

On estime l'énergie consommée par l'inférence en fonction du temps et de la puissance estimée du GPU/TPU :

$$E_{kWh} = \frac{t_{sec}}{3600} \times P_{device\_kW} \times PUE$$
$$CO2_{op} = E_{kWh} \times CI_{region}$$

  * **$P_{device}$** : Puissance thermique (TDP) estimée du matériel (ex: A100, TPU v4).
  * **PUE** : *Power Usage Effectiveness* (efficacité du data center).
  * **CI** : *Carbon Intensity* du mix électrique local.

### 2\. Part Matérielle / Embodied ($CO2_{hw}$)

On amortit le coût carbone de fabrication du serveur sur la durée de la requête :

$$CO2_{hw} = \frac{t_{sec}}{3600 \times Lifetime_{hours}} \times Carbon_{fabrication}$$

> [!NOTE]
> Pour chaque modèle et provider, les paramètres matériels sont définis dans `backend/config.py`. 

## 🏗️ Architecture du projet

```
├── app/
│   ├── 1_🏠_Accueil.py       # Point d'entrée Streamlit
│   └── pages/                # Pages auto-découvertes (CodeCarbon, etc.)
├── backend/
│   ├── config.py             # La "source de vérité" (Constantes, Modèles)
│   ├── llm_caller.py         # Wrappers API unifiés
│   └── compute_LLM_footprint.py # Le moteur de calcul CO2
├── data/                     # Stockage local (Prompts, Historique sessions)
└── emissions.csv             # Log généré par CodeCarbon
```

## 📄 Licence

Distribué sous licence MIT.

**Auteurs :** Chloé WIATT, Lucie CORREIA, Antoine BRETZNER