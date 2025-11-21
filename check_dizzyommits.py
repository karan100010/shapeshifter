#!/usr/bin/env python3
"""Check Dizzyommits branch for frontend code"""
import os
from github import Github, Auth
from dotenv import load_dotenv

# Load env vars
load_dotenv(os.path.join(os.path.dirname(__file__), 'issues', '.env'))
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')

if not TOKEN or not REPO_NAME:
    load_dotenv()
    TOKEN = os.getenv('GITHUB_TOKEN')
    REPO_NAME = os.getenv('GITHUB_REPO')

if not TOKEN or not REPO_NAME:
    print("Error: GITHUB_TOKEN or GITHUB_REPO not found.")
    exit(1)

print(f"Checking Dizzyommits branch in repo: {REPO_NAME}")
auth = Auth.Token(TOKEN)
g = Github(auth=auth)
repo = g.get_repo(REPO_NAME)

try:
    # Get contents of Dizzyommits branch
    print("\n=== DIZZYOMMITS BRANCH STRUCTURE ===\n")
    contents = repo.get_contents("", ref="Dizzyommits")
    
    def print_tree(contents, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        for content in contents:
            print(f"{prefix}+-- {content.name} ({'dir' if content.type == 'dir' else 'file'})")
            if content.type == "dir" and current_depth < max_depth - 1:
                try:
                    sub_contents = repo.get_contents(content.path, ref="Dizzyommits")
                    print_tree(sub_contents, prefix + "|   ", max_depth, current_depth + 1)
                except:
                    pass
    
    print_tree(contents)
    
    # Look for specific frontend files
    print("\n=== FRONTEND FILES DETECTED ===\n")
    
    def find_frontend_files(path="", ref="Dizzyommits"):
        try:
            contents = repo.get_contents(path, ref=ref)
            frontend_files = []
            
            for content in contents:
                if content.type == "file":
                    # Check for frontend-related files
                    if any(ext in content.name for ext in ['.html', '.jsx', '.tsx', '.vue', '.css', '.js']):
                        frontend_files.append(content.path)
                    if content.name in ['package.json', 'Dockerfile', 'docker-compose.yml', 'nginx.conf']:
                        frontend_files.append(content.path)
                elif content.type == "dir" and content.name not in ['.git', 'node_modules', '__pycache__']:
                    frontend_files.extend(find_frontend_files(content.path, ref))
            
            return frontend_files
        except:
            return []
    
    frontend_files = find_frontend_files()
    if frontend_files:
        for file in frontend_files[:20]:  # Show first 20
            print(f"  - {file}")
        if len(frontend_files) > 20:
            print(f"  ... and {len(frontend_files) - 20} more files")
    else:
        print("  No frontend files detected")
    
    # Check for Docker files
    print("\n=== DOCKER CONFIGURATION ===\n")
    try:
        dockerfile = repo.get_contents("Dockerfile", ref="Dizzyommits")
        print(f"[OK] Dockerfile found")
        print(f"  Size: {dockerfile.size} bytes")
    except:
        print("[X] No Dockerfile found")
    
    try:
        compose = repo.get_contents("docker-compose.yml", ref="Dizzyommits")
        print(f"[OK] docker-compose.yml found")
        print(f"  Size: {compose.size} bytes")
        print("\n  Content preview:")
        content_lines = compose.decoded_content.decode('utf-8').split('\n')
        for line in content_lines[:30]:
            print(f"    {line}")
    except:
        print("[X] No docker-compose.yml found")
        
except Exception as e:
    print(f"Error accessing Dizzyommits branch: {e}")

print("\nDone!")
