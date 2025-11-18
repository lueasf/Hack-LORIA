from openai import OpenAI
from google import genai
from groq import Groq
from .config import API_KEYS, MODELS_LIST

def call_openai(api_key, prompt, model):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

def call_gemini(api_key, prompt, model):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text

def call_groq(api_key, prompt, model):
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )

    return response.choices[0].message.content

def call_llm(provider, prompt, model):
    provider = provider.lower()
    api_key = ""

    # arguments communs
    kwargs = {"prompt": prompt}

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

# Exemple d'utilisation avec openai
if __name__ == "__main__":

    # Attention : pour tester ce script, il faut le lancer avec la commande suivante : python -m backend.llm_caller
    # impossible de le lancer directement car il fait partie d'un package
    provider = "openai"  # ou "gemini", "groq"
    model = "gpt-3.5-turbo"

    prompt = "Écris-moi un poème sur la lune."
    print("Appel du LLM avec le provider :", provider)
    
    result = call_llm(provider, prompt, model)
    print("Réponse du modèle :", result)