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

# Variables globales pour compute_LLM_footprint.py

HARDWARE_PROFILES = {
    "openai/gpt-3.5-turbo": {
        "device_count": 2,
        "device_power_kw": 0.6,
        "chip_type": "H100",
    },
}

PUE = 1.1

CARBON_INTENSITY = {
    "us": 0.4,   # kg CO2e / kWh
    "fr": 0.06,
}

FABRICATION_CO2 = {
    "CPU": 1.47,   # kg
    "DRAM": 102.4, # kg
    "SSD": 576.0,  # kg
    "H100": 14.652 # kg
}

TOTAL_HARDWARE_CO2 = sum(FABRICATION_CO2.values())  # kg

LIFETIME_HOURS = 4 * 365.25 * 24  # durée de vie matérielle en heures