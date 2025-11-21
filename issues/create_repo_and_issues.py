#!/usr/bin/env python3
"""
GitHub Repository Creator and Issue Filer
Creates the shapeshifter repository and files all issues
"""

import os
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not set")
    exit(1)

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
user = g.get_user()

print(f"Authenticated as: {user.login}")

# Create repository
repo_name = "shapeshifter"
repo_description = "RAG Enhanced Architecture - A production-ready Retrieval-Augmented Generation system with multi-agent orchestration, graph-based knowledge representation, and advanced retrieval strategies."

try:
    repo = user.get_repo(repo_name)
    print(f"Repository '{repo_name}' already exists")
except:
    print(f"Creating repository '{repo_name}'...")
    repo = user.create_repo(
        name=repo_name,
        description=repo_description,
        private=False,
        has_issues=True,
        has_wiki=True,
        has_projects=True,
        auto_init=True
    )
    print(f"[SUCCESS] Repository created: {repo.html_url}")

print(f"\nRepository: {repo.full_name}")
print(f"URL: {repo.html_url}")
print("\nReady to create issues!")
