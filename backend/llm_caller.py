from openai import OpenAI, APIError
from google import genai
from groq import Groq, APIError as GroqAPIError
from .config import API_KEYS, MODELS_LIST

def call_openai(api_key, prompt, model):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except APIError as e:
        # Gère toutes les erreurs venant de l'API OpenAI (authentification, rate limit, etc.)
        error_message = f"Erreur de l'API OpenAI : {e.status_code} - {e.message}"
        print(error_message)
        return {"error": error_message}
    except Exception as e:
        # Gère les autres erreurs (ex: problème de connexion)
        error_message = f"Une erreur inattendue est survenue avec OpenAI : {e}"
        print(error_message)
        return {"error": error_message}

def call_gemini(api_key, prompt, model):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt
            )
        return response.text
    except Exception as e:
        # La bibliothèque de Google peut lever des exceptions variées,
        # notamment pour des problèmes de permission (403), de ressource non trouvée (404) ou de surcharge (503).
        error_message = f"Une erreur est survenue avec l'API Gemini : {e}"
        print(error_message)
        return {"error": error_message}

def call_groq(api_key, prompt, model):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        return response.choices[0].message.content
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
        return {"error": f"Une erreur est survenue avec l'API Groq (code {e.status_code}). Veuillez réessayer plus tard."}
        
    except Exception as e:
        # Gère les autres erreurs (ex: problème de connexion)
        error_message = f"Une erreur inattendue est survenue avec Groq : {e}"
        print(error_message)
        return {"error": error_message}


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