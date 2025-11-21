# Vector DB setup script (requires Docker to run Qdrant container)
# See docs/docker_requirements.md for installation instructions

import subprocess
import shlex
import time
import os

# Configuration for Qdrant Docker container
DOCKER_IMAGE = "qdrant/qdrant"
HOST_PORT = "6333"
CONTAINER_NAME = "qdrant_vector_db"

def is_container_running(name: str) -> bool:
    """Check if a Docker container with the given name is already running."""
    try:
        result = subprocess.run(
            shlex.split(f"docker ps --filter name={name} --format '{{{{.Names}}}}'"),
            capture_output=True,
            text=True,
            check=True,
        )
        return name in result.stdout.strip().splitlines()
    except subprocess.CalledProcessError:
        return False

def start_qdrant_container() -> str:
    """Start a Qdrant Docker container and return its container ID."""
    if is_container_running(CONTAINER_NAME):
        print(f"[INFO] Container '{CONTAINER_NAME}' is already running.")
        result = subprocess.run(
            shlex.split(f"docker ps -aqf name={CONTAINER_NAME}"),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    print(f"[INFO] Starting Qdrant container '{CONTAINER_NAME}'...")
    cmd = f"docker run -d --name {CONTAINER_NAME} -p {HOST_PORT}:6333 {DOCKER_IMAGE}"
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
    container_id = result.stdout.strip()
    time.sleep(5)
    print(f"[SUCCESS] Qdrant container started with ID {container_id}")
    return container_id

def get_qdrant_endpoint() -> str:
    """Return the HTTP endpoint for the Qdrant service."""
    return f"http://localhost:{HOST_PORT}"

def setup_vector_db():
    """Initialize the vector database by ensuring the Docker container is running.
    Returns the endpoint URL for client connections.
    """
    start_qdrant_container()
    endpoint = get_qdrant_endpoint()
    print(f"[INFO] Qdrant endpoint available at {endpoint}")
    return endpoint

if __name__ == "__main__":
    # Ensure Docker is available
    try:
        subprocess.run(shlex.split("docker --version"), capture_output=True, check=True)
    except FileNotFoundError:
        print("[ERROR] Docker executable not found. Please install Docker and ensure it is in your PATH. See docs/docker_requirements.md for details.")
        exit(1)
    except Exception as e:
        print(f"[ERROR] Docker is not reachable: {e}. See docs/docker_requirements.md for troubleshooting.")
        exit(1)
    setup_vector_db()
