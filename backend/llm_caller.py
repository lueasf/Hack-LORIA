import os
import requests
from openai import OpenAI
from google import genai
from groq import Groq

def call_openai(api_key, prompt, model="gpt-3.5-turbo", temperature=0.7):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content

def call_gemini(api_key, prompt, model="gemini-2.5-flash"):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text

def call_groq(api_key, prompt, model="llama-3.3-70b-versatile"):
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
    )

    return response.choices[0].message.content

def call_llm(provider, api_key, prompt, model=""):
    provider = provider.lower()

    # arguments communs
    kwargs = {"api_key": api_key, "prompt": prompt}

    # ajouter model seulement s'il n'est pas vide
    if model:
        kwargs["model"] = model

    if provider == "openai":
        return call_openai(**kwargs)
    elif provider == "gemini":
        return call_gemini(**kwargs)
    elif provider == "groq":
        return call_groq(**kwargs)
    else:
        raise ValueError(f"Provider {provider} not supported.")

# Exemple d'utilisation avec openai
if __name__ == "__main__":
    provider = "openai"  # ou "gemini", "groq"
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Si besoin, on peut récupérer aussi les modèles depuis les variables d'environnement
    openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    prompt = "Écris-moi un poème sur la lune."
    print("Appel du LLM avec le provider :", provider)
    
    result = call_llm(provider, openai_api_key, prompt, model=openai_model)
    print("Réponse du modèle :", result)