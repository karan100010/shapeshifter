#!/usr/bin/env python3
"""
Push local files to GitHub repository using PyGithub.
Useful when local git client is not available.
"""

import os
from github import Github, Auth
from dotenv import load_dotenv
import base64

# Load env vars
load_dotenv(os.path.join(os.path.dirname(__file__), 'issues', '.env'))
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')

if not TOKEN or not REPO_NAME:
    # Try loading from current dir if issues/.env fails
    load_dotenv()
    TOKEN = os.getenv('GITHUB_TOKEN')
    REPO_NAME = os.getenv('GITHUB_REPO')

if not TOKEN or not REPO_NAME:
    print("Error: GITHUB_TOKEN or GITHUB_REPO not found in environment.")
    print("Please ensure .env file exists in 'issues' directory or current directory.")
    exit(1)

print(f"Authenticating with token for repo: {REPO_NAME}")
auth = Auth.Token(TOKEN)
g = Github(auth=auth)
repo = g.get_repo(REPO_NAME)

# Read .gitignore to create a filter
ignored_patterns = ['.git', '__pycache__', '.env', 'node_modules', '.DS_Store']
try:
    with open('.gitignore', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                ignored_patterns.append(line)
except FileNotFoundError:
    pass

def is_ignored(path):
    for pattern in ignored_patterns:
        if pattern in path or path.endswith(pattern):
            return True
    return False

# Walk through the directory
root_dir = os.getcwd()
print(f"Scanning directory: {root_dir}")

for root, dirs, files in os.walk(root_dir):
    # Remove ignored directories
    dirs[:] = [d for d in dirs if not is_ignored(d)]
    
    for file in files:
        if is_ignored(file):
            continue
            
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, root_dir).replace('\\', '/')
        
        if rel_path.startswith('.git/'):
            continue

        print(f"Processing: {rel_path}")
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            try:
                # Try to get existing file to update
                contents = repo.get_contents(rel_path)
                repo.update_file(contents.path, f"Update {rel_path}", content, contents.sha)
                print(f"  [UPDATED] {rel_path}")
            except:
                # File doesn't exist, create it
                repo.create_file(rel_path, f"Add {rel_path}", content)
                print(f"  [CREATED] {rel_path}")
                
        except Exception as e:
            print(f"  [ERROR] Failed to upload {rel_path}: {e}")

print("\nUpload complete!")
