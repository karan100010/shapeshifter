#!/usr/bin/env python3
"""
Add @kunaaall as a collaborator and tag front‑end issues.
Creates a "frontend" label (if missing) and adds a comment mentioning the user
on every issue that should be considered front‑end. For simplicity, we tag all
issues – you can adjust the filter logic later.
"""

import os
from github import Github, Auth
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPO')
CONTRIBUTOR = "kunaaall"

if not TOKEN or not REPO_NAME:
    raise SystemExit("Missing GITHUB_TOKEN or GITHUB_REPO in .env")

auth = Auth.Token(TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo(REPO_NAME)

# 1️⃣ Add collaborator (invite if not already a collaborator)
try:
    repo.add_to_collaborators(CONTRIBUTOR, permission='push')
    print(f"[+] Added @{CONTRIBUTOR} as collaborator (push permission).")
except Exception as e:
    print(f"[!] Could not add collaborator: {e}")

# 2️⃣ Ensure "frontend" label exists
label_name = "frontend"
label_color = "5319E7"  # purple, matches graph‑rag style
existing_labels = {lbl.name for lbl in repo.get_labels()}
if label_name not in existing_labels:
    try:
        repo.create_label(label_name, label_color)
        print(f"[+] Created label '{label_name}'.")
    except Exception as e:
        print(f"[!] Failed to create label: {e}")
else:
    print(f"[=] Label '{label_name}' already exists.")

# 3️⃣ Tag issues and comment @kunaaall
issues = repo.get_issues(state='open')
for issue in issues:
    # Add the frontend label if not present
    if label_name not in [lbl.name for lbl in issue.labels]:
        issue.add_to_labels(label_name)
        print(f"[+] Added label to issue #{issue.number}")
    # Add a comment mentioning the contributor
    comment_body = f"@{CONTRIBUTOR} – you are now assigned to this front‑end issue. Feel free to start working!"
    issue.create_comment(comment_body)
    print(f"[+] Commented on issue #{issue.number}")

print("\nAll done! Front‑end issues are now labelled and @kunaaall is mentioned.")
