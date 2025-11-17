import streamlit as st
import tempfile
import subprocess
import sys
import os
import time
import shutil
from codecarbon import EmissionsTracker

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
    project_name = st.text_input("Nom du projet (CodeCarbon)", value="streamlit_codecarbon")

uploaded_file = st.file_uploader("Upload .py file", type=["py"]) 
code_text = st.text_area("Ou collez votre code Python ici")

run = st.button("Run & measure")

if run:
    if uploaded_file is None and (not code_text or code_text.strip() == ""):
        st.warning("Veuillez uploader un fichier .py ou coller du code dans la zone de texte.")
    else:
        tmpdir = tempfile.mkdtemp(prefix="codecarbon_streamlit_")
        script_path = os.path.join(tmpdir, "script.py")
        repetitions = st.number_input("Répétitions (exécuter N fois)", min_value=1, value=1)
        intensity_override = st.number_input("Hypothèse intensité carbone (kg CO2/kWh)", min_value=0.0, value=0.3, format="%.3f")
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

            # Prepare tracker
            tracker = EmissionsTracker(project_name=project_name, output_dir=tmpdir, measure_power_secs=int(measure_power_secs))

            start_time = time.time()
            tracker.start()

            st.write("Execution en cours...")
            try:
                proc = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=int(timeout))
                run_stdout = proc.stdout
                run_stderr = proc.stderr
                returncode = proc.returncode
                timed_out = False
            except subprocess.TimeoutExpired as e:
                run_stdout = e.stdout or ""
                run_stderr = e.stderr or "Process timed out"
                returncode = -1
                timed_out = True
            except Exception as e:
                run_stdout = ""
                run_stderr = f"Erreur lors de l'exécution du script: {e}"
                returncode = -1
                timed_out = False

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
            try:
                # try to display as a float
                if isinstance(emissions, (float, int)):
                    st.metric(label="kg CO2eq", value=f"{emissions:.6f}")
                else:
                    # try to pretty-print
                    st.write(emissions)
            except Exception:
                st.write(repr(emissions))

            # show CSV if generated
            csv_path = os.path.join(tmpdir, "emissions.csv")
            if os.path.exists(csv_path):
                st.success(f"Fichier emissions CSV disponible: {csv_path}")
                with open(csv_path, "r", encoding="utf-8") as f:
                    csv_data = f.read()
                st.download_button("Télécharger emissions.csv", csv_data, file_name="emissions.csv", mime="text/csv")
            else:
                st.info("Aucun CSV généré par CodeCarbon dans le dossier temporaire.")

            st.write("---")
            st.write("Dossier temporaire (conserver pour debug):")
            st.code(tmpdir)

        finally:
            st.write("Vous pouvez supprimer le dossier temporaire manuellement si souhaité.")
            # on n'efface pas automatiquement pour laisser l'utilisateur récupérer le CSV en cas de besoin
            pass
