"""
Union AI / Flyte deployment wrapper for HTS Survey Explorer
"""
import subprocess
import os
from flytekit import task, workflow, Resources
from flytekit.types.file import FlyteFile

@task(
    requests=Resources(cpu="1", mem="1Gi"),
    limits=Resources(cpu="2", mem="2Gi"),
    container_image="python:3.9-slim"
)
def run_streamlit_app():
    """Launch the Streamlit app within Union AI infrastructure"""

    # Install dependencies
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

    # Run Streamlit app
    # Note: Union AI will handle port forwarding and URL generation
    subprocess.run([
        "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ])

@workflow
def deploy_hts_explorer():
    """Main workflow to deploy the app"""
    run_streamlit_app()

if __name__ == "__main__":
    # For local testing
    deploy_hts_explorer()