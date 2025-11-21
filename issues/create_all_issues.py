#!/usr/bin/env python3
"""
GitHub Issue Creator from CSV
Reads issues from CSV and creates them in GitHub
"""

import os
import csv
from github import Github, Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

if not GITHUB_TOKEN or not GITHUB_REPO:
    print("Error: Please set GITHUB_TOKEN and GITHUB_REPO environment variables")
    exit(1)

# Initialize GitHub client with new auth method
auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)
repo = g.get_repo(GITHUB_REPO)

print(f"Authenticated as: {g.get_user().login}")
print(f"Repository: {GITHUB_REPO}\n")

# Create labels first
labels_config = {
    "infrastructure": "0052CC",
    "storage": "1D76DB",
    "graph-rag": "5319E7",
    "agent": "D93F0B",
    "retrieval": "0E8A16",
    "deployment": "FBCA04",
    "testing": "C5DEF5",
    "documentation": "0075CA",
    "priority-high": "D73A4A",
    "priority-medium": "FBCA04",
    "priority-low": "0E8A16",
}

print("Creating labels...")
existing_labels = {label.name for label in repo.get_labels()}

for label_name, color in labels_config.items():
    if label_name not in existing_labels:
        try:
            repo.create_label(label_name, color)
            print(f"  [+] Created label: {label_name}")
        except Exception as e:
            print(f"  [!] Failed to create label {label_name}: {e}")
    else:
        print(f"  [=] Label exists: {label_name}")

# Read and create issues from CSV
print("\nReading issues from CSV...")
issues_created = 0
issues_failed = 0

with open('issues_bulk_import.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for idx, row in enumerate(reader, 1):
        title = row['Title'].strip()
        body = row['Body'].strip()
        labels_str = row['Labels'].strip()
        
        # Parse labels
        labels = [l.strip() for l in labels_str.split(',') if l.strip()]
        
        print(f"\n[{idx}] Creating issue: {title}")
        print(f"    Labels: {', '.join(labels)}")
        
        try:
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels
            )
            print(f"    [SUCCESS] Created issue #{issue.number}")
            issues_created += 1
        except Exception as e:
            print(f"    [ERROR] Failed: {e}")
            issues_failed += 1

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Issues created: {issues_created}")
print(f"  Issues failed: {issues_failed}")
print(f"  Total: {issues_created + issues_failed}")
print(f"{'='*60}")
print(f"\nRepository URL: https://github.com/{GITHUB_REPO}/issues")
