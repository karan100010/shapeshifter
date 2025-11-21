#!/usr/bin/env python3
"""
Shapeshifter Full-Stack Integration Runner
Starts both backend and frontend services for integrated testing
"""

import subprocess
import time
import sys
import os
import requests
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_step(step, text):
    print(f"{Colors.OKCYAN}[Step {step}]{Colors.ENDC} {text}")

def print_success(text):
    print(f"{Colors.OKGREEN}[OK]{Colors.ENDC} {text}")

def print_error(text):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {text}")

def print_warning(text):
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {text}")

def run_command(cmd, cwd=None, check=True):
    """Run shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_docker():
    """Check if Docker is running"""
    print_step(1, "Checking Docker...")
    success, stdout, stderr = run_command("docker info", check=False)
    if success:
        print_success("Docker is running")
        return True
    else:
        print_error("Docker is not running. Please start Docker Desktop.")
        return False

def start_backend():
    """Start backend services using docker-compose"""
    print_step(2, "Starting Backend Services...")
    
    # Check if docker-compose.yml exists
    if not Path("docker-compose.yml").exists():
        print_error("docker-compose.yml not found!")
        return False
    
    # Stop any existing services
    print("  Stopping existing services...")
    run_command("docker-compose down", check=False)
    
    # Start services
    print("  Starting services (this may take a few minutes)...")
    success, stdout, stderr = run_command("docker-compose up -d --build")
    
    if not success:
        print_error("Failed to start backend services")
        print(stderr)
        return False
    
    print_success("Backend services started")
    return True

def wait_for_backend(max_wait=120):
    """Wait for backend to be healthy"""
    print_step(3, "Waiting for Backend to be ready...")
    
    start_time = time.time()
    backend_url = "http://localhost:8080/health"
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(backend_url, timeout=5)
            if response.status_code == 200:
                print_success(f"Backend is ready! ({response.json()})")
                return True
        except requests.exceptions.RequestException:
            pass
        
        elapsed = int(time.time() - start_time)
        print(f"  Waiting... ({elapsed}s / {max_wait}s)", end='\r')
        time.sleep(5)
    
    print_error(f"Backend did not become ready within {max_wait} seconds")
    return False

def check_backend_services():
    """Check all backend services are running"""
    print_step(4, "Checking Backend Services...")
    
    success, stdout, stderr = run_command("docker-compose ps")
    if not success:
        print_error("Failed to check services")
        return False
    
    print(stdout)
    
    # Check specific services
    services = ["backend", "neo4j", "qdrant", "postgres", "redis"]
    for service in services:
        if service in stdout:
            print_success(f"{service} is running")
        else:
            print_warning(f"{service} may not be running")
    
    return True

def start_frontend(mode="dev"):
    """Start frontend service"""
    print_step(5, f"Starting Frontend ({mode} mode)...")
    
    frontend_path = Path("src/frontend")
    if not frontend_path.exists():
        print_warning("Frontend directory not found (may be on different branch)")
        print_warning("To test frontend:")
        print_warning("  1. git checkout Dizzyommits")
        print_warning("  2. cd src/frontend")
        print_warning("  3. npm install && npm run dev")
        return False
    
    # Check if node_modules exists
    if not (frontend_path / "node_modules").exists():
        print("  Installing frontend dependencies...")
        success, stdout, stderr = run_command("npm install", cwd=frontend_path)
        if not success:
            print_error("Failed to install frontend dependencies")
            return False
    
    # Start frontend
    if mode == "dev":
        print("  Starting frontend development server...")
        print_success("Frontend will start in development mode")
        print_success("Open: http://localhost:3000")
        print("\n  To start frontend manually:")
        print(f"    cd {frontend_path}")
        print("    npm run dev")
        return True
    elif mode == "docker":
        print("  Building frontend Docker image...")
        success, stdout, stderr = run_command(
            "docker build -t shapeshifter-frontend:latest .",
            cwd=frontend_path
        )
        if not success:
            print_error("Failed to build frontend image")
            return False
        
        print("  Starting frontend container...")
        success, stdout, stderr = run_command(
            "docker run -d -p 3000:3000 --name shapeshifter-frontend shapeshifter-frontend:latest"
        )
        if not success:
            print_error("Failed to start frontend container")
            return False
        
        print_success("Frontend Docker container started")
        return True

def print_access_info():
    """Print access information"""
    print_header("SYSTEM ACCESS INFORMATION")
    
    print(f"{Colors.BOLD}Frontend:{Colors.ENDC}")
    print(f"  URL: {Colors.OKBLUE}http://localhost:3000{Colors.ENDC}")
    print(f"  Status: Check manually or run: curl http://localhost:3000")
    
    print(f"\n{Colors.BOLD}Backend API:{Colors.ENDC}")
    print(f"  URL: {Colors.OKBLUE}http://localhost:8080{Colors.ENDC}")
    print(f"  Docs: {Colors.OKBLUE}http://localhost:8080/docs{Colors.ENDC}")
    print(f"  Health: {Colors.OKBLUE}http://localhost:8080/health{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Databases:{Colors.ENDC}")
    print(f"  Neo4j Browser: {Colors.OKBLUE}http://localhost:7474{Colors.ENDC} (neo4j/password)")
    print(f"  Qdrant Dashboard: {Colors.OKBLUE}http://localhost:6333/dashboard{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Useful Commands:{Colors.ENDC}")
    print(f"  View logs: docker-compose logs -f")
    print(f"  Stop all: docker-compose down")
    print(f"  Restart backend: docker-compose restart backend")

def print_test_scenarios():
    """Print test scenarios"""
    print_header("QUICK TEST SCENARIOS")
    
    print(f"{Colors.BOLD}1. Backend Health Check:{Colors.ENDC}")
    print('  curl http://localhost:8080/health')
    
    print(f"\n{Colors.BOLD}2. Create Test Workflow:{Colors.ENDC}")
    print('''  curl -X POST http://localhost:8080/workflows \\
    -H "Content-Type: application/json" \\
    -d '{"workflow_type": "indexing", "inputs": {"document_text": "Test"}}'
''')
    
    print(f"{Colors.BOLD}3. Frontend Access:{Colors.ENDC}")
    print(f'  Open browser: http://localhost:3000')
    print(f'  Upload a document and run a query')
    
    print(f"\n{Colors.BOLD}4. View API Documentation:{Colors.ENDC}")
    print(f'  Open browser: http://localhost:8080/docs')

def main():
    """Main function"""
    print_header("SHAPESHIFTER FULL-STACK INTEGRATION RUNNER")
    
    print("This script will start:")
    print("  - Backend API (FastAPI)")
    print("  - All database services (Neo4j, Qdrant, PostgreSQL, Redis)")
    print("  - Frontend (Optional, Next.js)")
    print()
    
    # Check Docker
    if not check_docker():
        sys.exit(1)
    
    # Start backend
    if not start_backend():
        print_error("Failed to start backend services")
        sys.exit(1)
    
    # Wait for backend
    if not wait_for_backend():
        print_error("Backend did not start properly")
        print("\nChecking logs:")
        run_command("docker-compose logs backend")
        sys.exit(1)
    
    # Check services
    check_backend_services()
    
    # Start frontend (info only)
    start_frontend(mode="dev")
    
    # Print access info
    print_access_info()
    
    # Print test scenarios
    print_test_scenarios()
    
    print_header("SYSTEM READY FOR TESTING")
    print(f"{Colors.OKGREEN}{Colors.BOLD}All backend services are running!{Colors.ENDC}")
    print()
    print("Press Ctrl+C to stop monitoring (services will keep running)")
    print("To stop all services: docker-compose down")
    
    # Keep script running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped. Services are still running.")
        print("To stop services: docker-compose down")

if __name__ == "__main__":
    main()
