from .config import HARDWARE_PROFILES, PUE, CARBON_INTENSITY, TOTAL_HARDWARE_CO2, LIFETIME_HOURS

def compute_carbon(model_name, prompt, response, tdev):
    """
    Stub pour calculer l'empreinte carbone.
    Remplace par ta vraie fonction.
    """

    # Si modèle inconnu
    profile = HARDWARE_PROFILES.get(model_name, {
        "device_count": 1, "device_power_kw": 0.5, "chip_type": "H100"
    })

    country = profile.get("country", "default")

    P = profile["device_count"] * profile["device_power_kw"]  # Puissance totale (kW)

    tdev_h = tdev / 3600  # conversion secondes -> heures

    # Calcul de l'empreinte carbone
    operational_carbon = P * PUE * CARBON_INTENSITY[country] * tdev_h

    hardware_carbon = (tdev_h / LIFETIME_HOURS) * TOTAL_HARDWARE_CO2

    total_carbon = (operational_carbon + hardware_carbon) * 1000 # Conversion en grammes

    return total_carbon