import streamlit as st
import tempfile
import subprocess
import sys
import os
import base64  # Ajout de l'import manquant
import time
from codecarbon import EmissionsTracker
import pandas as pd

project_name = "streamlit_codecarbon"

st.set_page_config(
    page_title="Carbon Footprint Analyzer for Code",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DÉBUT BLOC STYLE ACCUEIL ---
css_path = "app/accueil_styles.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        css_content = f.read()
    
    st.markdown(f"""
        <style>
            {css_content}
            .stApp {{
                /* Dégradé du vert clair vers un vert plus soutenu */
                background: linear-gradient(135deg, #94a773 0%, #94a45a 100%);
                background-attachment: fixed;
            }}
            /* Styles spécifiques pour les cartes de cette page (adaptés de styles.css) */
            .metric-card {{
                background: rgba(255, 255, 255, 0.6);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                margin-bottom: 1rem;
            }}
            .comparison-item {{
                background: rgba(255, 255, 255, 0.6);
                padding: 1rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                border-left: 4px solid #7fb069;
            }}

            /* --- NOUVEAU : Style pour les expanders (menus déroulants) en blanc --- */
            [data-testid="stExpander"] {{
                background-color: #ffffff !important;
                border-radius: 8px !important;
                border: none !important;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                color: #000000 !important;
            }}
            [data-testid="stExpander"] summary {{
                color: #000000 !important;
            }}
            [data-testid="stExpander"] summary:hover {{
                color: #333333 !important;
            }}
            /* Force la couleur du texte à l'intérieur en noir */
            [data-testid="stExpander"] p, [data-testid="stExpander"] li, [data-testid="stExpander"] span, [data-testid="stExpander"] div {{
                color: #000000 !important;
            }}
        </style>
    """, unsafe_allow_html=True)

# 2. Barre de navigation simplifiée (Juste le logo)
st.markdown("""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 70px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    padding: 0 2rem;
    z-index: 999998;
">
    <div style="margin-left: 2rem; font-size: 1.5rem; font-weight: 700; color: #000000; font-family: 'Righteous', sans-serif;">
        TelecomCarbon 🌿
    </div>
</div>
<div style='margin-top: 3rem;'></div>
""", unsafe_allow_html=True)
# --- FIN BLOC STYLE ACCUEIL ---

st.markdown('<h1>Carbon Footprint Analyzer for Code</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Mesurez précisément l\'empreinte carbone de vos scripts et commandes avec CodeCarbon</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Configuration")
    
    st.markdown("### Paramètres d'exécution")
    timeout = st.number_input("Timeout (secondes)", min_value=1, value=60, help="Durée maximale d'exécution autorisée")
    measure_power_secs = st.number_input("Intervalle de mesure (s)", min_value=1, value=1, help="Fréquence d'échantillonnage de la puissance")
    repetitions = st.number_input("Répétitions", min_value=1, value=1, help="Nombre d'exécutions pour améliorer la précision")
    
    st.markdown("---")
    
    st.markdown("### Mode d'exécution")
    run_mode = st.selectbox(
        "Type de code",
        ["Script Python", "Autre"],
        help="Choisissez Python pour du code Python, ou Autre pour n'importe quelle commande shell"
    )
    
    st.markdown("---")
    
    st.markdown("### Ressources")
    st.markdown("[Documentation CodeCarbon](https://codecarbon.io/)")
    st.markdown("[Sources méthodologie](https://github.com/mlco2/codecarbon)")

# Main content area
col_space1, col_upload, col_or, col_space2 = st.columns([1, 2, 0.5, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Uploader un fichier",
        type=["py"],
        help="Sélectionnez un fichier .py à analyser"
    )

with col_or:
    st.markdown("### ")  # Spacing
    st.markdown("<div style='text-align: center;'>ou</div>", unsafe_allow_html=True)

code_text = st.text_area(
    "Code source",
    height=200,
    placeholder="Collez votre code Python ici...",
    help="Entrez directement votre code à analyser"
)

command_text = st.text_input(
    "Commande (mode 'Autre')",
    placeholder="Ex: javac code.java && java Main",
    help="Commande shell à exécuter et mesurer"
)

st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run = st.button("Analyser l'empreinte carbone", use_container_width=True)

if run:
    if run_mode == "Script Python":
        if uploaded_file is None and (not code_text or code_text.strip() == ""):
            st.warning("Veuillez uploader un fichier .py ou coller du code dans la zone de texte pour le mode 'Script Python'.")
            st.stop()
    else:
        if not command_text or command_text.strip() == "":
            st.warning("Veuillez fournir une commande à exécuter pour le mode 'Commande arbitraire'.")
            st.stop()

    tmpdir = tempfile.mkdtemp(prefix="codecarbon_streamlit_")
    script_path = os.path.join(tmpdir, "script.py")
    try:
        if run_mode == "Script Python":
            if uploaded_file is not None:
                content = uploaded_file.read()
                if isinstance(content, bytes):
                    content = content.decode("utf-8")
            else:
                content = code_text
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(content)
            st.info(f"Script enregistré dans : {script_path}")

        st.write("---")

        run_stdout = ""
        run_stderr = ""
        returncode = 0
        timed_out = False

        with EmissionsTracker(project_name=project_name, output_dir=tmpdir, measure_power_secs=int(measure_power_secs)) as tracker:
            start_time = time.time()
            st.write("Exécution en cours...")

            for i in range(int(repetitions)):
                try:
                    if run_mode == "Autre":
                        cmd = command_text.strip()
                        proc = subprocess.run(cmd, shell=True, cwd=tmpdir, capture_output=True, text=True, timeout=int(timeout))
                    else:
                        proc = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=int(timeout))

                    run_stdout += f"\n--- Run {i+1} stdout ---\n" + (proc.stdout or "")
                    run_stderr += f"\n--- Run {i+1} stderr ---\n" + (proc.stderr or "")
                    returncode = proc.returncode
                except subprocess.TimeoutExpired as e:
                    run_stdout += f"\n--- Run {i+1} stdout (partial) ---\n" + (e.stdout or "")
                    run_stderr += f"\n--- Run {i+1} stderr ---\n" + (e.stderr or "Process timed out")
                    returncode = -1
                    timed_out = True
                    break
                except Exception as e:
                    run_stdout += f"\n--- Run {i+1} stdout (error) ---\n"
                    run_stderr += f"\n--- Run {i+1} stderr ---\nErreur lors de l'exécution: {e}"
                    returncode = -1
                    timed_out = False
                    break

            try:
                emissions = tracker.stop()
            except Exception:
                emissions = None
            end_time = time.time()
            duration = end_time - start_time

        # path to CSV (available after tracker run)
        csv_path = os.path.join(tmpdir, "emissions.csv")

        st.markdown("---")
        st.markdown("## Résultats de l'exécution")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            status_text = "Succès" if returncode == 0 else "Erreur"
            st.metric("Statut", f"{status_text} (code {returncode})")
        with col_res2:
            st.metric("Durée", f"{duration:.3f} s")
        with col_res3:
            st.metric("Répétitions", int(repetitions))
        
        if timed_out:
            st.error("Le script a dépassé le timeout spécifié.")

        with st.expander("Voir la sortie standard (stdout)", expanded=False):
            st.code(run_stdout, language="text")
        with st.expander("Voir les erreurs (stderr)", expanded=False):
            st.code(run_stderr, language="text")

        st.markdown("---")
        st.markdown("## Empreinte carbone")

        emissions_kg = None
        try:
            if isinstance(emissions, (float, int)):
                emissions_kg = float(emissions)
            else:
                emissions_kg = float(emissions)
        except Exception:
            emissions_kg = None

        if emissions_kg is not None:
            emissions_g = emissions_kg * 1000.0
            
            # Affichage principal de l'émission
            col_main1, col_main2 = st.columns([1, 2])
            with col_main1:
                st.metric(
                    label="Émissions totales",
                    value=f"{emissions_g:.6f} g",
                    delta=f"CO₂eq",
                    help="Grammes de CO₂ équivalent émis"
                )
            with col_main2:
                total_g = emissions_g
                avg_g = total_g / max(1, int(repetitions))
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 0.9rem; color: #a0aec0; margin-bottom: 0.5rem;">DÉTAILS</div>
                    <div style="font-size: 1.1rem; color: #e2e8f0;">
                        <strong>Total:</strong> {total_g:.6f} g CO₂eq<br>
                        <strong>Par exécution:</strong> {avg_g:.6f} g CO₂eq
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Try to estimate energy (kWh) precisely: prefer CSV fields if available, else derive from emissions using a default intensity
            energy_kwh = None
            df2 = None
            try:
                if os.path.exists(csv_path):
                    df2 = pd.read_csv(csv_path)
                    if 'energy_consumed' in df2.columns:
                        energy_kwh = float(df2['energy_consumed'].iloc[-1])
                    elif 'estimated_energy_Wh' in df2.columns:
                        energy_kwh = float(df2['estimated_energy_Wh'].iloc[-1]) / 1000.0
                    else:
                        # try to compute from last reported powers
                        power_sum_local = 0.0
                        if 'cpu_power' in df2.columns:
                            power_sum_local += float(df2['cpu_power'].iloc[-1] or 0.0)
                        if 'ram_power' in df2.columns:
                            power_sum_local += float(df2['ram_power'].iloc[-1] or 0.0)
                        if 'gpu_power' in df2.columns:
                            power_sum_local += float(df2['gpu_power'].iloc[-1] or 0.0)
                        if power_sum_local > 0.0:
                            energy_kwh = power_sum_local * float(duration) / 3600.0
            except Exception:
                energy_kwh = None

            # fallback: derive energy from emissions using an intensity value (g CO2 / kWh)
            if energy_kwh is None:
                intensity_g_per_kwh = None
                try:
                    if df2 is not None:
                        for col in ('carbon_intensity', 'intensity', 'grid_intensity', 'carbon_intensity_g_per_kwh'):
                            if col in df2.columns:
                                intensity_g_per_kwh = float(df2[col].iloc[-1])
                                break
                except Exception:
                    intensity_g_per_kwh = None
                if intensity_g_per_kwh is None:
                    intensity_g_per_kwh = 475.0  # fallback world-average g CO2 / kWh
                energy_kwh = float(total_g) / float(intensity_g_per_kwh)

            # Human-friendly comparisons using energy_kwh where possible
            st.markdown("### Équivalences")
            
            st.markdown('<div style="margin-top: 1.5rem;">', unsafe_allow_html=True)

            # Car: use a default factor (g CO2 per km) and show a small plausible range
            car_g_per_km = 120.0
            car_low = 95.0
            car_high = 150.0
            km_equiv = total_g / car_g_per_km
            km_equiv_low = total_g / car_high
            km_equiv_high = total_g / car_low
            meters_equiv = km_equiv * 1000.0
            
            st.markdown(f"""
            <div class="comparison-item">
                <strong>Transport automobile</strong><br>
                {km_equiv:.3f} km (plage: {km_equiv_low:.3f}–{km_equiv_high:.3f} km)<br>
                <span style="color: #a0aec0; font-size: 0.9rem;">≈ {meters_equiv:.0f} mètres parcourus</span>
            </div>
            """, unsafe_allow_html=True)

            # Energy-based comparisons
            energy_wh = energy_kwh * 1000.0
            
            # smartphone ~10 Wh
            smartphone_wh = 10.0
            smartphone_charges = energy_wh / smartphone_wh
            
            st.markdown(f"""
            <div class="comparison-item">
                <strong>Énergie consommée</strong><br>
                {energy_kwh:.4f} kWh = {smartphone_charges:.3f} charges de smartphone<br>
                <span style="color: #a0aec0; font-size: 0.9rem;">Basé sur une batterie de ~10 Wh</span>
            </div>
            """, unsafe_allow_html=True)

            # laptop ~30 W -> minutes = energy_wh / 30 * 60
            laptop_w = 30.0
            laptop_minutes = (energy_wh / laptop_w) * 60.0
            
            st.markdown(f"""
            <div class="comparison-item">
                <strong>Utilisation laptop</strong><br>
                {laptop_minutes:.1f} minutes<br>
                <span style="color: #a0aec0; font-size: 0.9rem;">Basé sur une consommation moyenne de {laptop_w:.0f} W</span>
            </div>
            """, unsafe_allow_html=True)

            # LED 10W seconds
            led_w = 10.0
            led_seconds = (energy_wh / led_w) * 3600.0
            
            st.markdown(f"""
            <div class="comparison-item">
                <strong>Éclairage LED</strong><br>
                {led_seconds:.1f} secondes<br>
                <span style="color: #a0aec0; font-size: 0.9rem;">LED {led_w:.0f} W allumée</span>
            </div>
            """, unsafe_allow_html=True)

            # 100 W incandescent bulb minutes
            bulb100_w = 100.0
            bulb100_minutes = (energy_wh / bulb100_w) * 60.0
            
            st.markdown(f"""
            <div class="comparison-item">
                <strong>Ampoule incandescente</strong><br>
                {bulb100_minutes:.2f} minutes<br>
                <span style="color: #a0aec0; font-size: 0.9rem;">Ampoule {bulb100_w:.0f} W allumée</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Impossible de convertir les émissions en valeurs numériques (non disponible).")

        st.markdown("---")
        st.markdown("## Données détaillées")
        
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                csv_data = f.read()
            
            col_csv1, col_csv2 = st.columns([2, 1])
            with col_csv1:
                st.success(f"Fichier emissions.csv généré")
            with col_csv2:
                st.download_button(
                    "Télécharger CSV",
                    csv_data,
                    file_name="emissions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            try:
                df = pd.read_csv(csv_path)
                summary = {}
                summary['runs_executed'] = int(repetitions)
                summary['duration_s'] = float(duration)

                emissions_from_df = None
                if 'emissions' in df.columns:
                    emissions_from_df = float(df['emissions'].iloc[-1])
                elif 'co2_emissions' in df.columns:
                    emissions_from_df = float(df['co2_emissions'].iloc[-1])

                if emissions_kg is not None:
                    summary['emissions_kg'] = float(emissions_kg)
                    summary['emissions_g'] = float(emissions_kg * 1000.0)
                elif emissions_from_df is not None:
                    summary['emissions_kg'] = emissions_from_df
                    summary['emissions_g'] = emissions_from_df * 1000.0

                for key in ('cpu_power', 'gpu_power', 'ram_power'):
                    if key in df.columns:
                        summary[key + '_last'] = float(df[key].iloc[-1])
                for key in ('os', 'python_version', 'ram_total_size', 'codecarbon_version', 'water_consumed'):
                    if key in df.columns:
                        summary[key] = df[key].iloc[-1]

                power_sum = 0.0
                has_power = False
                if 'cpu_power' in df.columns:
                    power_sum += float(df['cpu_power'].iloc[-1] or 0.0)
                    has_power = True
                if 'ram_power' in df.columns:
                    power_sum += float(df['ram_power'].iloc[-1] or 0.0)
                    has_power = True
                if 'gpu_power' in df.columns:
                    power_sum += float(df['gpu_power'].iloc[-1] or 0.0)
                    has_power = True

                if has_power:
                    est_energy_wh = power_sum * float(duration) / 3600.0
                    summary['estimated_energy_Wh'] = est_energy_wh

                if summary:
                    summary_df = pd.DataFrame(list(summary.items()), columns=['Métrique', 'Valeur'])
                    st.markdown("### Résumé technique")
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)

            except Exception as e:
                st.warning(f"Erreur lors du parsing du CSV: {e}")
        else:
            st.info("Aucun CSV généré par CodeCarbon dans le dossier temporaire.")

        with st.expander("Informations de débogage", expanded=False):
            st.code(f"Dossier temporaire: {tmpdir}", language="text")
            st.caption("Vous pouvez supprimer ce dossier manuellement si nécessaire.")
    
    except Exception as e:
        st.error(f"Une erreur est survenue: {e}")

st.markdown("---")

st.markdown("---")

with st.expander("Méthodologie technique", expanded=False):
    st.markdown("""

    ### Processus de mesure
    
    **1. Validation et préparation**  
    Le script est validé à l'entrée et sauvegardé dans un dossier temporaire où seront placés les fichiers de sortie.
    
    **2. Mesure encapsulée**  
    L'exécution se fait sous un contexte `EmissionsTracker` qui démarre automatiquement et garantit l'arrêt du scheduler.
    
    ```python
    with EmissionsTracker(project_name=..., output_dir=tmpdir, measure_power_secs=...) as tracker:
    ```
    
    **3. Échantillonnage et capteurs**  
    Un scheduler échantillonne la puissance CPU/GPU/RAM selon l'intervalle configuré. CodeCarbon utilise prioritairement des capteurs matériels (RAPL sur Linux, powermetrics sur macOS). En leur absence, il retombe sur une estimation via TDP + charge CPU.
    
    **4. Calcul et sortie**  
    La puissance (W) est intégrée dans le temps pour obtenir l'énergie (Wh → kWh), convertie en émissions via l'intensité carbone locale, et journalisée dans `emissions.csv`.
    ```text
    E ~ Σ P_moy x Δt
    ```
                
    **5. Résultats et limites**  
    L'application agrège les totaux et propose des comparaisons. Les mesures courtes ou sans accès RAPL sont moins précises.
    
    ### Sources des équivalences
    - **CodeCarbon**: [Documentation officielle](https://codecarbon.io/) | [GitHub](https://github.com/mlco2/codecarbon)
    """)

st.markdown('<div style="text-align: center; padding: 2rem 0; color: #a0aec0; font-size: 0.9rem;">Carbon Footprint Analyzer • Par Lucie, Chloé et Antoine</div>', unsafe_allow_html=True)
