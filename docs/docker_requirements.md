# Docker Requirements for Local Development

This project requires Docker to be installed and running locally for the following components:

- **Qdrant (Vector Database)**: Used for storing and searching embeddings.
- **Neo4j (Graph Database)**: Used for knowledge graph storage.
- **PostgreSQL (Metadata Store)**: Used for workflow state persistence.
- **Redis (Cache & Rate Limiting)**: Used for caching and rate limiting.

## Installation

1. **Install Docker Desktop**:
   - Windows: Download from https://www.docker.com/products/docker-desktop
   - macOS: Download from https://www.docker.com/products/docker-desktop
   - Linux: Follow the instructions for your distribution (e.g., `apt-get install docker.io`).
2. **Verify Installation**:
   ```bash
   docker --version
   ```
   The command should output the Docker version without errors.
3. **Start Docker**:
   Ensure the Docker daemon is running before executing any setup scripts.

## Usage

All setup scripts (e.g., `src/vector_db/setup.py`, `src/graph/setup.py`, etc.) will check for Docker availability and exit with a clear error message if Docker is not found. Please install Docker and retry.
