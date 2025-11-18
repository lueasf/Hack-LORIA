import json
from pathlib import Path

def load_json(path: Path):
    try:
        # Spécifie l'encodage UTF-8 lors de la lecture
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError: # Capturer l'erreur spécifique si le fichier n'existe pas
        return []
    except json.JSONDecodeError: # Capturer l'erreur si le contenu n'est pas un JSON valide
        print(f"Warning: Failed to decode JSON from {path}. Returning empty list.")
        return []
    except Exception as e: # Capturer d'autres erreurs inattendues
        print(f"An unexpected error occurred while loading {path}: {e}")
        return []

def save_json(path: Path, data): # Ajout de l'annotation de type pour clarifier
    # Spécifie l'encodage UTF-8 lors de l'écriture
    # Et utilise ensure_ascii=False pour éviter l'échappement des caractères non-ASCII
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')