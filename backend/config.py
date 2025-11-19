import os
from dotenv import load_dotenv

load_dotenv()

# Keys
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "gemini": os.getenv("GEMINI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY"),
    "hf": os.getenv("HUGGINGFACE_API_KEY"),
}

# Models lists
MODELS_LIST = {
    "openai": os.getenv("OPENAI_MODEL", "").split(","),
    "gemini": os.getenv("GEMINI_MODEL", "").split(","),
    "groq": os.getenv("GROQ_MODEL", "").split(","),
    "hf": os.getenv("HUGGINGFACE_MODEL", "").split(","),
}

# Variables globales pour compute_LLM_footprint.py

HARDWARE_PROFILES = {
    "llama-3.3-70b-versatile": {
        "device_count": 576,          # Un "Pod" Groq complet (souvent 8 racks de 72 puces)
        "device_power_kw": 0.185,     # ~185W par puce LPU (hors refroidissement rack)
        "chip_type": "Groq LPU Gen1", # Language Processing Unit
        "notes": "Architecture massivement parallèle sur SRAM pour latence ultra-faible.",
        "country": "us"
    },

    "llama-3.3-70b": {
        "device_count": 576,          
        "device_power_kw": 0.185,
        "chip_type": "Groq LPU Gen1",
        "notes": "Même configuration que le modèle 'versatile', optimisé pour inférence batch.",
        "country": "us"
    },

    "gpt-3.5-turbo": {
        "device_count": 8,            # Un noeud standard DGX/HGX
        "device_power_kw": 0.7,       # ~700W max par H100 (ou 400W si A100)
        "chip_type": "H100 NVL",      # Souvent migré sur H100 pour l'efficacité FP8
        "notes": "Configuration dense, probablement 8 GPUs servant de multiples requêtes en batch.",
        "country": "us"
    },
    
    "gpt-4": {
        "device_count": 16,           # Cluster de 2 noeuds HGX H100 (16 GPUs totaux)
        "device_power_kw": 0.7,
        "chip_type": "H100 NVL",
        "notes": "Inférence distribuée sur cluster nécessaire pour la VRAM totale.",
        "country": "us"
    },

    "gemini-2.5-flash": {
        "device_count": 4,            # Une "slice" TPU v5e (v5e-4)
        "device_power_kw": 0.25,      # ~250W par puce TPU v5e
        "chip_type": "TPU v5e",       # Tensor Processing Unit v5e (optimisé inférence)
        "notes": "Modèle optimisé pour tenir sur une petite topologie de puces.",
        "country": "us"
    },
    "deepseek-ai/DeepSeek-V3.1:novita": {
        "device_count": 16,           # Nécessite ~2 noeuds H100 (ou 1 noeud H200) pour tenir en VRAM
        "device_power_kw": 0.7,       # ~700W par H100 NVL/SXM5
        "chip_type": "H100 NVL",      # Indispensable pour l'accélération FP8 (Transformer Engine)
        "notes": "Modèle 671B MoE. En FP8 (config), pèse ~671Go. Ne tient pas sur un seul noeud H100 80Go (640Go total). Requiert du parallélisme inter-noeuds (TP/EP).",
        "country": "cn"
    },

    "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai": {
        "device_count": 1,            # Tient largement sur un seul GPU
        "device_power_kw": 0.35,      # ~350W (Profil A100 PCIe ou L40S)
        "chip_type": "NVIDIA A100",   # Ou L40S, souvent utilisé pour les petits modèles (7B)
        "notes": "Modèle dense 7B (15Go en BF16). Sur Featherless (serverless), une seule instance GPU charge le modèle et sert les requêtes via une file d'attente.",
        "country": "fr"
    }
}

PUE = 1.1

CARBON_INTENSITY = {
    "default": 0.4,   # kg CO2e / kWh
    "us": 0.4,
    "fr": 0.06,
    "cn": 0.55
}

FABRICATION_CO2 = {
    "CPU": 1.47,   # kg
    "DRAM": 102.4, # kg
    "SSD": 576.0,  # kg
    "H100": 14.652 # kg
}

TOTAL_HARDWARE_CO2 = sum(FABRICATION_CO2.values())  # kg

LIFETIME_HOURS = 4 * 365.25 * 24  # durée de vie matérielle en heures