import streamlit as st
from backend.compute_LLM_footprint import compute_carbon
from backend.config import (
    HARDWARE_PROFILES,
    PUE,
    CARBON_INTENSITY,
    TOTAL_HARDWARE_CO2,
    LIFETIME_HOURS,
)

def show_calculation():
    st.set_page_config(page_title="Comprendre l'empreinte", layout="wide")
    
    st.markdown(
        """
        Ce calculateur utilise la méthodologie **LLMCarbon**, qui prend en compte :
        1. **L'empreinte opérationnelle** (consommation dynamique selon les FLOPs et le matériel).
        2. **L'empreinte 'embodied'** (coût de fabrication du hardware amorti sur la durée d'usage).
        
        Source : [LLMCarbon: Modeling the End-to-End Carbon Footprint of Large Language Models (arXiv:2309.14393)](https://arxiv.org/abs/2309.14393)
        """
    )

    # --- 1. Récupération des données (identique à ton code) ---
    session_model = st.session_state.get("selected_model", None)
    
    # Fallback si pas de modèle
    if session_model is None:
        st.warning("Mode démonstration (pas de modèle sélectionné).")
        session_model = "gpt-3.5-turbo" # Exemple par défaut

    # Profil matériel
    profile = HARDWARE_PROFILES.get(session_model, {"device_count": 1, "device_power_kw": 0.5, "chip_type": "H100 (Default)"})
    
    # Données d'exécution
    tdev = st.session_state.get("last_tdev", 0.73) # Valeur par défaut pour l'exemple
    region_used = profile.get("country", "default")
    
    # --- 2. Pré-calculs pour l'affichage ---
    device_count = int(profile.get("device_count", 1))
    device_power_kw = float(profile.get("device_power_kw", 0.5))
    chip_name = profile.get("chip_type", "GPU")
    
    # Puissance
    total_power_kw = device_count * device_power_kw
    
    # Temps
    tdev_seconds = float(tdev)
    tdev_hours = tdev_seconds / 3600.0
    
    # Facteurs carbones
    ci_val = CARBON_INTENSITY.get(region_used, CARBON_INTENSITY[region_used]) # kgCO2e/kWh
    
    # A. Calcul Opérationnel (Énergie)
    # Formule : Puissance * PUE * Intensité Carbone * Temps
    operational_carbon_kg = total_power_kw * PUE * ci_val * tdev_hours
    
    # B. Calcul Matériel (Embodied)
    # Formule : (Temps d'usage / Durée de vie) * Coût fabrication total
    hardware_carbon_kg = (tdev_hours / LIFETIME_HOURS) * TOTAL_HARDWARE_CO2
    
    # Total
    total_carbon_g = (operational_carbon_kg + hardware_carbon_kg) * 1000.0

    # --- 3. Affichage Créatif ---

    st.divider()

    # Le Résultat Héroïque
    c_res1, c_res2, c_res3 = st.columns([1, 2, 1])
    with c_res2:
        st.metric(
            label="Empreinte Totale de la requête",
            value=f"{total_carbon_g:.4f} gCO2e",
            delta="Résultat final",
            delta_color="off"
        )

    st.divider()
    
    # On utilise deux grandes colonnes pour séparer les concepts
    col_energy, col_hardware = st.columns(2)

    with col_energy:
        st.subheader("⚡ La Consommation Électrique")
        st.info("C'est l'électricité brûlée par les cartes graphiques (GPU) et le refroidissement pendant que l'IA réfléchit.")
        
        st.markdown(f"""
        * **Matériel utilisé** : {device_count} x {chip_name}
        * **Puissance brute** : {total_power_kw} kW
        * **Efficacité du datacenter (PUE)** : x {PUE} (le surcoût du refroidissement)
        * **Durée du calcul** : {tdev_seconds:.3f} secondes
        """)
        
        st.markdown("#### La formule :")
        st.latex(r'''
           E_{éléc} = P_{uissance} \times PUE \times Temps \times Intensité_{Réseau}
        ''')
        
        st.write(f"L'intensité carbone de la région ({region_used}) est de **{ci_val} kgCO2e/kWh**.")
        
        st.success(f"**Impact Énergie :** {operational_carbon_kg*1000:.4f} gCO2e")

    with col_hardware:
        st.subheader("🏭 L'Amortissement Matériel")
        st.info("La fabrication des serveurs émet énormément de CO2. On attribue une infime fraction de ce coût à votre requête.")
        
        percent_usage = (tdev_hours / LIFETIME_HOURS) * 100
        st.markdown(f"""
        * **Coût de fabrication serveur** : {TOTAL_HARDWARE_CO2:.0f} kgCO2e
        * **Durée de vie estimée** : {LIFETIME_HOURS:,.0f} heures
        * **Votre temps d'usage** : {tdev_seconds:.3f} secondes
        """)
        
        st.markdown("#### La formule :")
        st.latex(r'''
           E_{matériel} = \frac{Temps_{usage}}{Durée_{vie}} \times Empreinte_{Fabrication}
        ''')
        
        st.write(f"Votre requête représente **{percent_usage:.10f} %** de la vie du serveur.")
        
        st.warning(f"**Impact Matériel :** {hardware_carbon_kg*1000:.4f} gCO2e")

    st.divider()

if __name__ == "__main__":
    show_calculation()