# Hackathon LORIA
Cette application example montre comment mesurer l'empreinte carbone d'un script Python en utilisant
`codecarbon`, via une interface Streamlit.

Fichiers ajoutés dans ce dépôt :

- `streamlit_app.py` — application Streamlit. Elle permet d'uploader un script `.py` ou de coller du
	code, exécute le script sous `EmissionsTracker` de CodeCarbon, et affiche :
	- le résultat en kg CO2eq (si retourné par CodeCarbon),
	- la durée d'exécution,
	- stdout / stderr du script,
	- proposition de téléchargement du `emissions.csv` (si généré).
- `requirements.txt` — listes des dépendances (streamlit, codecarbon, psutil).

Important — sécurité

L'application exécute du code Python fourni par l'utilisateur sur la machine hôte. Ne lancez
jamais de code non fiable sur un environnement de production. Pour exécuter du code non-trusté,
utilisez un sandbox (ex : conteneur Docker isolé, VM, ou service dédié).

Installation et exécution

1. Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Lancez l'application Streamlit :

```bash
streamlit run streamlit_app.py
```

Utilisation

- Uploadez un script `.py` ou collez le code dans la zone prévue.
- Réglez le timeout et l'intervalle de mesure si besoin.
- Cliquez sur "Run & measure". L'app affichera stdout/stderr, la durée, et la valeur retournée
	par CodeCarbon (kg CO2eq). Si CodeCarbon a généré un `emissions.csv`, il sera proposé en téléchargement.

Prochaines améliorations possibles

- Ajouter un sandbox (docker) pour exécuter du code non fiable en sécurité.
- Afficher des graphiques à partir des données du CSV (mesures par intervalle).
- Permettre d'exécuter seulement une fonction du script plutôt que le script entier.

Contact

Projet préparé pour un hackathon. Pour questions ou améliorations, ouvrez une issue.