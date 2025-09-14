
import shlex
import subprocess
from pathlib import Path
import os
import modal


streamlit_script_local_path = Path(__file__).parent / "project_streamlit.py"
streamlit_script_remote_path = "/root/project_streamlit.py"


image = (
    modal.Image.debian_slim(python_version="3.9")
    .uv_pip_install("streamlit", "supabase", "pandas", "plotly")
    .env({"FORCE_REBUILD": "true"})  # optional, forces rebuild
    .add_local_file(streamlit_script_local_path, streamlit_script_remote_path)
)


# You must add SUPABASE_KEY and SUPABASE_URL in Modal's secret manager
app = modal.App(name="usage-dashboard", image=image)

if not streamlit_script_local_path.exists():
    raise RuntimeError("Streamlit script not found!")

@app.function(
    allow_concurrent_inputs=100,
    secrets=[modal.Secret.from_name("supabase")]
)
@modal.web_server(8000)
def run():
    # Prepare the command to run Streamlit
    target = shlex.quote(streamlit_script_remote_path)
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"

   
    env_vars = dict(os.environ)  # include current environment
    env_vars["SUPABASE_KEY"] = os.environ["SUPABASE_KEY"]
    env_vars["SUPABASE_URL"] = os.environ["SUPABASE_URL"]

    subprocess.Popen(cmd, shell=True, env=env_vars)
