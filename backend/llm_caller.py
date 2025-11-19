from openai import OpenAI, APIError
from google import genai
from groq import Groq, APIError as GroqAPIError
from .config import API_KEYS, MODELS_LIST

import requests
import time

def call_openai(api_key, prompt, model):
    try:
        client = OpenAI(api_key=api_key)
        start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        tdev = time.time() - start
        return response.choices[0].message.content, tdev
    except APIError as e:
        # Gère toutes les erreurs venant de l'API OpenAI (authentification, rate limit, etc.)
        error_message = f"Erreur de l'API OpenAI : {e.status_code} - {e.message}"
        print(error_message)
        return {"error": error_message}, 0
    except Exception as e:
        # Gère les autres erreurs (ex: problème de connexion)
        error_message = f"Une erreur inattendue est survenue avec OpenAI : {e}"
        print(error_message)
        return {"error": error_message}, 0

def call_gemini(api_key, prompt, model):
    try:
        client = genai.Client(api_key=api_key)
        start = time.time()
        response = client.models.generate_content(
            model=model,
            contents=prompt
            )
        tdev = time.time() - start
        return response.text, tdev
    except Exception as e:
        # La bibliothèque de Google peut lever des exceptions variées,
        # notamment pour des problèmes de permission (403), de ressource non trouvée (404) ou de surcharge (503).
        error_message = f"Une erreur est survenue avec l'API Gemini : {e}"
        print(error_message)
        return {"error": error_message}, 0

def call_groq(api_key, prompt, model):
    try:
        client = Groq(api_key=api_key)
        start = time.time()
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        tdev = time.time() - start
        return response.choices[0].message.content, tdev
    except GroqAPIError as e:
        error_details = "Détails non disponibles"
        
        if e.body:
            if isinstance(e.body, dict):
                # Cas 1 : L'erreur est un JSON propre, on l'analyse
                error_details = e.body.get('error', {}).get('message', str(e.body))
            else:
                # Cas 2 : L'erreur n'est pas un dictionnaire (string, HTML...)
                body_str = str(e.body).strip()
                
                # On vérifie si la chaîne ressemble à du HTML
                if body_str.lower().startswith('<!doctype html'):
                    # Si c'est du HTML, on crée un message d'erreur clair et concis
                    error_details = (
                        "Le service a rencontré une erreur interne (probablement une erreur 5xx de Cloudflare). "
                        "Le service est peut-être temporairement indisponible."
                    )
                else:
                    # Si c'est une autre chaîne, on l'affiche (en la tronquant si elle est trop longue)
                    error_details = (body_str[:250] + '...') if len(body_str) > 250 else body_str
        
        # Ce message est pour les logs côté backend
        full_error_message = f"Erreur de l'API Groq : {e.status_code} - {error_details}"
        print(full_error_message)
        
        # On retourne un message simple et propre pour le front-end
        return {"error": f"Une erreur est survenue avec l'API Groq (code {e.status_code}). Veuillez réessayer plus tard."}, 0
        
    except Exception as e:
        # Gère les autres erreurs (ex: problème de connexion)
        error_message = f"Une erreur inattendue est survenue avec Groq : {e}"
        print(error_message)
        return {"error": error_message}, 0
    


HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

def call_HF(api_key: str, prompt: str, model: str):
    """
    Envoie un message utilisateur vers l'API Inference de Hugging Face.
    Gère les erreurs réseaux, les erreurs d'API (4xx, 5xx) et le chargement des modèles.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False # On force le non-streaming pour simplifier la réponse
    }

    try:
        start = time.time()
        # On ajoute un timeout pour éviter que le script ne pende indéfiniment
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        # Gestion des codes d'erreur HTTP (4xx, 5xx)
        if response.status_code != 200:
            error_details = response.text
            
            # Tentative d'extraction propre du message d'erreur JSON renvoyé par HF
            try:
                error_json = response.json()
                # HF renvoie souvent {'error': 'Model is loading...'} ou {'error': ['msg...']}
                if isinstance(error_json, dict) and 'error' in error_json:
                    error_details = error_json['error']
            except ValueError:
                # Si ce n'est pas du JSON (ex: page HTML d'erreur 502 Bad Gateway)
                pass

            # Gestion spécifique : Modèle en cours de chargement (Erreur 503 fréquente sur HF)
            if response.status_code == 503 and "loading" in str(error_details).lower():
                print(f"Info HF : Le modèle {model} est en cours de chargement (Cold Boot).")
                return {"error": "Le modèle est en cours de chargement sur les serveurs Hugging Face. Veuillez réessayer dans 20-30 secondes."}, 0
            
            error_message = f"Erreur de l'API HF : {response.status_code} - {error_details}"
            print(error_message)
            return {"error": f"Une erreur est survenue avec Hugging Face (code {response.status_code})."}, 0

        # Succès
        data = response.json()
        tdev = time.time() - start
        
        # Vérification que la structure de réponse est celle attendue
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"], tdev
        else:
            print(f"Format de réponse inattendu de HF : {data}")
            return {"error": "Format de réponse inattendu de l'API Hugging Face."}, 0

    except requests.exceptions.Timeout:
        error_message = "Erreur : La requête vers Hugging Face a expiré (Timeout)."
        print(error_message)
        return {"error": error_message}, 0

    except requests.exceptions.ConnectionError:
        error_message = "Erreur : Impossible de se connecter aux serveurs Hugging Face (Problème réseau)."
        print(error_message)
        return {"error": error_message}, 0

    except Exception as e:
        # Capture toute autre erreur imprévue (parsing, etc.)
        error_message = f"Une erreur inattendue est survenue avec HF : {e}"
        print(error_message)
        return {"error": error_message}, 0

def call_llm(provider, prompt, model=None):
    provider = provider.lower()
    api_key = ""

    # arguments communs
    kwargs = {"prompt": prompt}

    try:
        if provider == "openai":
            api_key = API_KEYS["openai"]
            model = model if model else MODELS_LIST["openai"][0]
            kwargs["api_key"] = api_key
            kwargs["model"] = model
            return call_openai(**kwargs)
        elif provider == "gemini":
            api_key = API_KEYS["gemini"]
            model = model if model else MODELS_LIST["gemini"][0]
            kwargs["model"] = model
            kwargs["api_key"] = api_key
            return call_gemini(**kwargs)
        elif provider == "groq":
            api_key = API_KEYS["groq"]
            model = model if model else MODELS_LIST["groq"][0]
            kwargs["model"] = model
            kwargs["api_key"] = api_key
            return call_groq(**kwargs)
        elif provider == "hf":
            api_key = API_KEYS["hf"]
            model = model if model else MODELS_LIST["hf"][0]
            kwargs["model"] = model
            kwargs["api_key"] = api_key
            return call_HF(**kwargs)
        else:
            raise ValueError(f"Provider {provider} not supported.")
    except KeyError as e:
        error_message = f"Clé API ou configuration de modèle manquante pour le provider '{provider}' : {e}"
        print(error_message)
        return {"error": error_message}
    except ValueError as e:
        # Gère le cas où le provider n'est pas supporté
        print(e)
        return {"error": str(e)}
    except Exception as e:
        # Capture toute autre erreur imprévue
        error_message = f"Une erreur générale est survenue dans call_llm : {e}"
        print(error_message)
        return {"error": error_message}


# Exemple d'utilisation avec openai
if __name__ == "__main__":

    # Attention : pour tester ce script, il faut le lancer avec la commande suivante : python -m backend.llm_caller
    # impossible de le lancer directement car il fait partie d'un package
    provider = "groq"  # ou "gemini", "groq"
    model = ""

    prompt = "Écris-moi un poème sur la lune."
    print("Appel du LLM avec le provider :", provider)
    
    result = call_llm(provider, prompt, model)

    # Le front-end devra vérifier si la réponse est un dictionnaire avec une clé 'error'
    if isinstance(result, dict) and 'error' in result:
        print("Une erreur a été retournée :", result['error'])
    else:
        print("Réponse du modèle :", result)