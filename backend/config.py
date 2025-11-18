import os
from dotenv import load_dotenv

load_dotenv()

# Keys
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY"),
}

# Models lists
MODELS_LIST = {
    "openai": os.getenv("OPENAI_MODEL", "").split(","),
    "gemini": os.getenv("GEMINI_MODEL", "").split(","),
    "groq": os.getenv("GROQ_MODEL", "").split(","),
}
