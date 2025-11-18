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
    "llama-3.3-70b-versatile": {
        "device_count": 576,          # Un "Pod" Groq complet (souvent 8 racks de 72 puces)
        "device_power_kw": 0.185,     # ~185W par puce LPU (hors refroidissement rack)
        "chip_type": "Groq LPU Gen1", # Language Processing Unit
        "notes": "Architecture massivement parallèle sur SRAM pour latence ultra-faible."
    },

    "llama-3.3-70b": {
        "device_count": 576,          
        "device_power_kw": 0.185,
        "chip_type": "Groq LPU Gen1",
        "notes": "Même configuration que le modèle 'versatile', optimisé pour inférence batch."
    },

    "gpt-3.5-turbo": {
        "device_count": 8,            # Un noeud standard DGX/HGX
        "device_power_kw": 0.7,       # ~700W max par H100 (ou 400W si A100)
        "chip_type": "H100 NVL",      # Souvent migré sur H100 pour l'efficacité FP8
        "notes": "Configuration dense, probablement 8 GPUs servant de multiples requêtes en batch."
    },
    
    "gpt-4": {
        "device_count": 16,           # Cluster de 2 noeuds HGX H100 (16 GPUs totaux)
        "device_power_kw": 0.7,
        "chip_type": "H100 NVL",
        "notes": "Inférence distribuée sur cluster nécessaire pour la VRAM totale."
    },

    "gemini-2.5-flash": {
        "device_count": 4,            # Une "slice" TPU v5e (v5e-4)
        "device_power_kw": 0.25,      # ~250W par puce TPU v5e
        "chip_type": "TPU v5e",       # Tensor Processing Unit v5e (optimisé inférence)
        "notes": "Modèle optimisé pour tenir sur une petite topologie de puces."
    }
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