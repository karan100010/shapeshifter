# Neo4j Graph setup script (requires Docker to run Neo4j container)
# See docs/docker_requirements.md for installation instructions

import subprocess
import shlex
import time
import os

# Configuration for Neo4j Docker container
DOCKER_IMAGE = "neo4j:5"
HOST_PORT = "7687"
HTTP_PORT = "7474"
CONTAINER_NAME = "neo4j_graph_db"

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

def start_neo4j_container() -> str:
    """Start a Neo4j Docker container and return its container ID."""
    if is_container_running(CONTAINER_NAME):
        print(f"[INFO] Container '{CONTAINER_NAME}' is already running.")
        result = subprocess.run(
            shlex.split(f"docker ps -aqf name={CONTAINER_NAME}"),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    print(f"[INFO] Starting Neo4j container '{CONTAINER_NAME}'...")
    cmd = (
        f"docker run -d --name {CONTAINER_NAME} -p {HOST_PORT}:7687 -p {HTTP_PORT}:7474 "
        f"-e NEO4J_AUTH=neo4j/password {DOCKER_IMAGE}"
    )
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, check=True)
    container_id = result.stdout.strip()
    time.sleep(5)
    print(f"[SUCCESS] Neo4j container started with ID {container_id}")
    return container_id

def get_neo4j_bolt_endpoint() -> str:
    """Return the Bolt endpoint for Neo4j."""
    return f"bolt://localhost:{HOST_PORT}"

def get_neo4j_http_endpoint() -> str:
    """Return the HTTP endpoint for Neo4j Browser/API."""
    return f"http://localhost:{HTTP_PORT}"

def setup_neo4j():
    """Initialize Neo4j by ensuring the Docker container is running and return endpoints."""
    start_neo4j_container()
    bolt = get_neo4j_bolt_endpoint()
    http = get_neo4j_http_endpoint()
    print(f"[INFO] Neo4j Bolt endpoint: {bolt}")
    print(f"[INFO] Neo4j HTTP endpoint: {http}")
    return bolt, http

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
    setup_neo4j()
