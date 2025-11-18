from openai import OpenAI
from google import genai
from groq import Groq
from backend.config import API_KEYS, MODELS_LIST

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

def call_llm(provider, prompt, model=""):
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
    provider = "openai"  # ou "gemini", "groq"

    prompt = "Écris-moi un poème sur la lune."
    print("Appel du LLM avec le provider :", provider)
    
    result = call_llm(provider, prompt)
    print("Réponse du modèle :", result)