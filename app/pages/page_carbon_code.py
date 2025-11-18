import streamlit as st
import tempfile
import subprocess
import sys
import os
import time
from codecarbon import EmissionsTracker
import pandas as pd

project_name = "streamlit_codecarbon"

st.set_page_config(page_title="Mesure d'empreinte avec CodeCarbon", layout="wide")
st.title("Mesure d'empreinte carbone d'un script avec CodeCarbon")

st.markdown(
    "Uploadez un fichier Python ou collez votre code et fournissez une commande à exécuter, puis cliquez sur \"Run & measure\".\n\n"
)

with st.sidebar:
    st.header("Options")
    timeout = st.number_input("Timeout (secondes)", min_value=1, value=60)
    measure_power_secs = st.number_input("Intervalle de mesure (s)", min_value=1, value=1)
    repetitions = st.number_input("Répétitions (exécuter N fois)", min_value=1, value=1)
    st.markdown("---")
    st.markdown("Mode d'exécution : choisissez si vous voulez exécuter un script Python (upload/coller) ou un script d'un autre langage.")
    run_mode = st.selectbox("Mode d'exécution", ["Script Python", "Autre"])

uploaded_file = st.file_uploader("Upload .py file", type=["py"]) 
code_text = st.text_area("Ou collez votre code ici")
command_text = st.text_input("Commande à exécuter (pour mode 'Autre')")

run = st.button("Run & measure")

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
            st.write("Execution en cours...")

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
            st.metric(label="g CO2eq", value=f"{emissions_g:.6f}")
            total_g = emissions_g
            avg_g = total_g / max(1, int(repetitions))
            st.write(f"**Total:** {total_g:.6f} g CO2eq - **Par run (moyenne):** {avg_g:.6f} g")

            meters_car = (total_g / 120.0) * 1000.0
            st.write("#### Comparaisons (approximatives)")
            st.write(f"~ {meters_car:.2f} mètres en voiture (~120 g CO2/km)")
        else:
            st.info("Impossible de convertir les émissions en valeurs numériques (non disponible).")

        csv_path = os.path.join(tmpdir, "emissions.csv")
        if os.path.exists(csv_path):
            st.success(f"Fichier emissions CSV disponible: {csv_path}")
            with open(csv_path, "r", encoding="utf-8") as f:
                csv_data = f.read()
            st.download_button("Télécharger emissions.csv", csv_data, file_name="emissions.csv", mime="text/csv")

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
                    summary_df = pd.DataFrame(list(summary.items()), columns=['metric', 'value'])
                    st.write("#### Résumé")
                    st.table(summary_df)

            except Exception as e:
                st.info(f"Erreur lors du parsing du CSV: {e}")
        else:
            st.info("Aucun CSV généré par CodeCarbon dans le dossier temporaire.")

        st.write("---")
        st.write("Dossier temporaire (conserver pour debug):")
        st.code(tmpdir)

    finally:
        st.write("Vous pouvez supprimer le dossier temporaire manuellement si souhaité.")
        pass

with st.expander("Détails techniques : comment l'application mesure et calcule"):
    st.markdown("""
    Le script est validé à l'entrée et on crée un dossier temporaire où le déposer.

    Nous initialisons ensuite le contexte de mesure :

    ```python
    with EmissionsTracker(project_name=..., output_dir=tmpdir, measure_power_secs=...) as tracker:
    ```

    Cette ligne instancie le tracker et le démarre à l'entrée du `with` (équivalent à `tracker.start()`), puis l'arrête automatiquement à la sortie (`tracker.stop()`). Par défaut, les résultats sont loggés dans `emissions.csv` dans `output_dir`.

    Ce que CodeCarbon met en place au démarrage :
    - Le tracker crée un `ResourceTracker` et un scheduler périodique qui échantillonne la puissance toutes les `measure_power_secs` secondes (15s par défaut dans CodeCarbon; ici on permet d'utiliser 1s). Cet échantillonnage est la base du calcul d'énergie.
    - Il choisit les capteurs selon la machine : sur CPU il tentera d'abord une mesure matérielle (RAPL sur Linux, `powermetrics` sur macOS). Si ces capteurs sont indisponibles comme sur WSL par exemple, CodeCarbon bascule en mode de repli : il mappe votre CPU à une base de TDP (Intel/AMD) puis estime la puissance à partir du TDP et de la charge CPU (via `psutil`).
    - Il prépare la sortie (un "output sink") : par défaut un `FileOutput` qui écrira des lignes dans `emissions.csv`.
    - Il résout le contexte géographique (pays / cloud) pour obtenir un facteur d'intensité carbone (g CO₂/kWh).

    Pendant que le script tourne :
    - L'application lance N fois l'exécution via `subprocess.run(...)`). Pendant cette période, le scheduler continue d'échantillonner CPU/GPU/RAM (sur l'ensemble de la machine en mode par défaut), cumule l'énergie et journalise les mesures.
    - À chaque tick, CodeCarbon convertit la puissance instantanée (W) en énergie (Wh) par intégration temporelle :

    ```text
    E ~ Σ P_moy x Δt
    ```

    Il s'agit de la somme des puissances moyennes sur chaque intervalle multipliées par la durée de l'intervalle).

    - L'énergie totale (kWh) est ensuite multipliée par l'intensité carbone locale (g CO₂/kWh) pour produire les émissions (g CO₂e).

    À la sortie du `with` (arrêt) : `tracker.stop()` arrête le scheduler, vide les dernières mesures, calcule les totaux (énergie, émissions) et retourne les émissions totales en kg CO₂e (l'application convertit ensuite en grammes pour l'affichage).

    Contenu du CSV final : selon la configuration et la plateforme, vous trouverez typiquement des colonnes telles que `timestamp`, `emissions` (kg), `emissions_rate`, `energy_consumed` (kWh), `cpu_power` / `gpu_power` / `ram_power` (W) et des métadonnées (OS, version Python, pays / zone, cloud, etc.). L'application lit ce CSV, calcule des agrégats (total, moyenne par run) et affiche une comparaison (ex. voiture) basée sur un facteur de ~120 g CO₂/km.

    """)
