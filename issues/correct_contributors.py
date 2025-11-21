#!/usr/bin/env python3
"""
Corrects contributors:
1. Removes 'kunaaall' (wrong user)
2. Adds 'kunaaalll' (correct user)
3. Assigns 'karan100010' to backend issues (Infrastructure, Agents, Storage, etc.)
4. Creates/Updates a Frontend issue and assigns 'kunaaalll'
"""

import os
from github import Github, Auth
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')

WRONG_USER = "kunaaall"
CORRECT_USER = "kunaaalll"
BACKEND_USER = "karan100010"

if not TOKEN or not REPO_NAME:
    raise SystemExit("Missing GITHUB_TOKEN or GITHUB_REPO in .env")

auth = Auth.Token(TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo(REPO_NAME)

print(f"Repository: {REPO_NAME}")

# 1. Manage Collaborators
print(f"\n--- Managing Collaborators ---")
try:
    repo.remove_from_collaborators(WRONG_USER)
    print(f"[+] Removed {WRONG_USER}")
except Exception as e:
    print(f"[-] Could not remove {WRONG_USER} (might not be a collaborator): {e}")

try:
    repo.add_to_collaborators(CORRECT_USER, permission='push')
    print(f"[+] Added {CORRECT_USER} as collaborator")
except Exception as e:
    print(f"[!] Failed to add {CORRECT_USER}: {e}")

# 2. Manage Issues
print(f"\n--- Updating Issues ---")
issues = repo.get_issues(state='open')

# Define backend labels
backend_labels = {'infrastructure', 'storage', 'agent', 'retrieval', 'deployment', 'testing', 'graph-rag'}

frontend_issue_found = False

for issue in issues:
    labels = {l.name for l in issue.labels}
    
    # Check if it's a backend issue
    if labels.intersection(backend_labels) or 'documentation' in labels:
        # It's likely backend/core
        if 'frontend' in labels:
            issue.remove_from_labels('frontend')
            print(f"  [Clean] Removed 'frontend' label from #{issue.number} {issue.title}")
        
        # Assign Karan
        if BACKEND_USER not in [a.login for a in issue.assignees]:
            issue.add_to_assignees(BACKEND_USER)
            print(f"  [Assign] Assigned {BACKEND_USER} to #{issue.number}")
            
    # Check for potential frontend issues (or create one if none exist)
    if 'frontend' in labels or 'dashboard' in issue.title.lower() or 'ui' in issue.title.lower():
        frontend_issue_found = True
        # Assign Kunal
        if CORRECT_USER not in [a.login for a in issue.assignees]:
            issue.add_to_assignees(CORRECT_USER)
            print(f"  [Assign] Assigned {CORRECT_USER} to frontend issue #{issue.number}")
        
        # Tag him
        issue.create_comment(f"@{CORRECT_USER} - This is the correct issue for you. Please ignore previous tags to the other account.")

# 3. Create Frontend Issue if missing
if not frontend_issue_found:
    print(f"\n--- Creating Frontend Issue ---")
    try:
        # Ensure label exists
        try:
            repo.create_label("frontend", "5319E7")
        except:
            pass

        body = f"""Implement the Frontend Dashboard for the RAG system.
        
**Requirements:**
- User Interface for query input
- Visualization of retrieval results (Graph & Vector)
- System status monitoring
- Chat interface for Agent interactions

**Assignee:** @{CORRECT_USER}
"""
        issue = repo.create_issue(
            title="Frontend Dashboard Implementation",
            body=body,
            labels=["frontend", "priority-high"],
            assignees=[CORRECT_USER]
        )
        print(f"[+] Created Frontend Issue #{issue.number} and assigned {CORRECT_USER}")
        issue.create_comment(f"@{CORRECT_USER} - Welcome! This is your main tracking issue.")
        
    except Exception as e:
        print(f"[!] Failed to create frontend issue: {e}")

print("\nDone! Contributors corrected and issues updated.")
