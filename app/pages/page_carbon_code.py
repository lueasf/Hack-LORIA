import streamlit as st
import tempfile
import subprocess
import sys
import os
import time
import shutil
import math
from codecarbon import EmissionsTracker

# optional pandas for CSV table/plot
try:
    import pandas as pd
except Exception:
    pd = None

# fixed project name (removed option from sidebar as requested)
project_name = "streamlit_codecarbon"

st.set_page_config(page_title="Mesure d'empreinte (CodeCarbon)", layout="wide")
st.title("Mesure d'empreinte carbone d'un script Python (CodeCarbon)")

st.markdown(
    "Uploadez un fichier Python ou collez votre code, puis cliquez sur \"Run & measure\".\n\n"
    "Attention : le code sera exécuté sur la machine qui héberge l'application — ne lancez pas de code non fiable."
)

with st.sidebar:
    st.header("Options")
    timeout = st.number_input("Timeout (secondes)", min_value=1, value=60)
    measure_power_secs = st.number_input("Intervalle de mesure (s)", min_value=1, value=1)
    repetitions = st.number_input("Répétitions (exécuter N fois)", min_value=1, value=1)

uploaded_file = st.file_uploader("Upload .py file", type=["py"]) 
code_text = st.text_area("Ou collez votre code Python ici")

run = st.button("Run & measure")

if run:
    if uploaded_file is None and (not code_text or code_text.strip() == ""):
        st.warning("Veuillez uploader un fichier .py ou coller du code dans la zone de texte.")
    else:
        tmpdir = tempfile.mkdtemp(prefix="codecarbon_streamlit_")
        script_path = os.path.join(tmpdir, "script.py")
        try:
            # write the code
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

            # Prepare tracker and run inside context to ensure it stops cleanly
            run_stdout = ""
            run_stderr = ""
            returncode = 0
            timed_out = False

            with EmissionsTracker(project_name=project_name, output_dir=tmpdir, measure_power_secs=int(measure_power_secs)) as tracker:
                start_time = time.time()
                st.write("Execution en cours...")

                # execute script N times to accumulate measurable emissions
                for i in range(int(repetitions)):
                    try:
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
                        run_stderr += f"\n--- Run {i+1} stderr ---\nErreur lors de l'exécution du script: {e}"
                        returncode = -1
                        timed_out = False
                        break

                # stop tracker and collect emissions
                emissions = tracker.stop()
                end_time = time.time()
                duration = end_time - start_time

            st.write("### Résultats de l'exécution")
            st.write(f"Return code: `{returncode}`")
            st.write(f"Durée mesurée: `{duration:.3f}` s")
            if timed_out:
                st.error("Le script a dépassé le timeout spécifié.")

            with st.expander("Stdout"):
                st.code(run_stdout)
            with st.expander("Stderr"):
                st.code(run_stderr)

            st.write("---")
            st.write("### Résultats CodeCarbon")

            # emissions can be float or other object depending on version; handle gracefully
            emissions_kg = None
            try:
                if isinstance(emissions, (float, int)):
                    emissions_kg = float(emissions)
                    emissions_g = emissions_kg * 1000.0
                    st.metric(label="g CO2eq", value=f"{emissions_g:.6f}")
                else:
                    try:
                        emissions_kg = float(emissions)
                        emissions_g = emissions_kg * 1000.0
                        st.metric(label="g CO2eq", value=f"{emissions_g:.6f}")
                    except Exception:
                        st.write(emissions)
            except Exception:
                st.write(repr(emissions))

            # convert to grams for comparisons
            if emissions_kg is not None:
                total_g = emissions_kg * 1000.0
                avg_g = total_g / max(1, int(repetitions))
                st.write(f"**Total:** {total_g:.6f} g CO2eq — **Par run (moyenne):** {avg_g:.6f} g")

                # other comparisons (no intensity hypothesis)
                meters_car = (total_g / 120.0) * 1000.0  # assuming 120 g CO2 per km

                st.write("#### Comparaisons (approximatives)")
                st.write(f"≈ {meters_car:.2f} mètres en voiture (~120 g CO2/km)")
            else:
                st.info("Impossible de convertir les émissions en valeurs numériques (non disponible).")

            # show CSV if generated and display table with interval info
            csv_path = os.path.join(tmpdir, "emissions.csv")
            if os.path.exists(csv_path):
                st.success(f"Fichier emissions CSV disponible: {csv_path}")
                with open(csv_path, "r", encoding="utf-8") as f:
                    csv_data = f.read()
                st.download_button("Télécharger emissions.csv", csv_data, file_name="emissions.csv", mime="text/csv")

                if pd is not None:
                    try:
                        df = pd.read_csv(csv_path)

                        # Build a compact summary using available fields
                        summary = {}
                        summary['runs_executed'] = int(repetitions)
                        summary['duration_s'] = float(duration)

                        # prefer emissions column name 'emissions' then 'co2_emissions'
                        emissions_from_df = None
                        if 'emissions' in df.columns:
                            emissions_from_df = float(df['emissions'].iloc[-1])
                        elif 'co2_emissions' in df.columns:
                            emissions_from_df = float(df['co2_emissions'].iloc[-1])

                        # fill summary from tracker or csv
                        if emissions_kg is not None:
                            summary['emissions_kg'] = float(emissions_kg)
                            summary['emissions_g'] = float(emissions_kg * 1000.0)
                        elif emissions_from_df is not None:
                            summary['emissions_kg'] = emissions_from_df
                            summary['emissions_g'] = emissions_from_df * 1000.0

                        # add some hardware/info fields if present
                        for key in ('cpu_power', 'gpu_power', 'ram_power'):
                            if key in df.columns:
                                summary[key + '_last'] = float(df[key].iloc[-1])
                        for key in ('os', 'python_version', 'ram_total_size', 'codecarbon_version', 'water_consumed'):
                            if key in df.columns:
                                summary[key] = df[key].iloc[-1]

                        # If we have power and duration, estimate energy (Wh)
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
                            # energy (Wh) ~ power (W) * duration(s) / 3600
                            est_energy_wh = power_sum * float(duration) / 3600.0
                            summary['estimated_energy_Wh'] = est_energy_wh

                        # Present summary table
                        if summary:
                            summary_df = pd.DataFrame(list(summary.items()), columns=['metric', 'value'])
                            st.write("#### Résumé compact")
                            st.table(summary_df)

                        # Add human-friendly comparisons based on emissions_g and estimated energy
                        try:
                            emissions_g_val = summary.get('emissions_g')
                            if emissions_g_val is not None:
                                st.write("#### Comparaisons basées sur les émissions")
                                st.write(f"Emissions totales : {emissions_g_val:.6f} g CO2eq")
                                meters_car = (emissions_g_val / 120.0) * 1000.0
                                st.write(f"≈ {meters_car:.2f} mètres en voiture (~120 g CO2/km)")
                                # smartphone charge approx 10 Wh and other comparisons
                                if 'estimated_energy_Wh' in summary:
                                    est_wh = summary['estimated_energy_Wh']
                                    try:
                                        st.write(f"Énergie estimée ≈ {est_wh:.4f} Wh")
                                        # smartphone full charge ~10 Wh
                                        smartphone_charges = est_wh / 10.0
                                        st.write(f"Ce code utilise autant d'énergie que ~{smartphone_charges:.3f} charges complètes de smartphone (~10 Wh)")

                                        # laptop consumption ~30 W -> minutes = Wh/30 * 60 = Wh * 2
                                        laptop_minutes = est_wh * 2.0
                                        st.write(f"≈ {laptop_minutes:.1f} minutes d'utilisation d'un laptop (~30 W)")

                                        # 100 W incandescent bulb minutes
                                        bulb100_minutes = (est_wh / 100.0) * 60.0
                                        st.write(f"≈ {bulb100_minutes:.2f} minutes d'une ampoule 100 W")

                                        # boil 1 L ~100 Wh (0.1 kWh) approximate
                                        liters_boil = est_wh / 100.0
                                        st.write(f"≈ {liters_boil:.4f} litre(s) d'eau chauffé(s) (1L ≈ 100 Wh)")

                                        # LED 10W seconds
                                        led10_seconds = (est_wh / 10.0) * 3600.0
                                        st.write(f"≈ {led10_seconds:.1f} secondes d'une LED 10 W")
                                    except Exception:
                                        pass
                        except Exception:
                            pass

                    except Exception as e:
                        st.info(f"Erreur lors du parsing du CSV: {e}")
                else:
                    st.info("Installez pandas pour afficher le tableau des mesures (voir requirements).")
            else:
                st.info("Aucun CSV généré par CodeCarbon dans le dossier temporaire.")

            st.write("---")
            st.write("Dossier temporaire (conserver pour debug):")
            st.code(tmpdir)

        finally:
            st.write("Vous pouvez supprimer le dossier temporaire manuellement si souhaité.")
            # on n'efface pas automatiquement pour laisser l'utilisateur récupérer le CSV en cas de besoin
            pass
