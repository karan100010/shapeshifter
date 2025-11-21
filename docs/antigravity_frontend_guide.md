# Antigravity Front‑End Contributor Guide

## 🎯 Goal
Help **@kunaaall** get up‑to‑speed quickly on working with the front‑end related GitHub issues in the **shapeshifter** repository using the Antigravity IDE.

## 📋 Prerequisites
1. **GitHub account** (already invited as a collaborator).
2. **Antigravity IDE** installed – see the official install guide in the repo’s `README.md`.
3. **Python 3.11+** (for running the helper scripts).
4. **Personal Access Token** with `repo` scope (the same token you used for issue creation).

## 🔧 Setup Steps
### 1️⃣ Clone the Repository
```bash
# Open a terminal inside Antigravity IDE
git clone https://github.com/karan100010/shapeshifter.git
cd shapeshifter
```

### 2️⃣ Install Project Dependencies
```bash
# Inside the repo root
pip install -r requirements.txt   # (if a requirements file exists)
# Or install the minimal deps you need for the scripts
pip install PyGithub python-dotenv
```

### 3️⃣ Create a `.env` File (if not present)
```text
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=karan100010/shapeshifter
```
> **⚠️** The `.env` file is already listed in `.gitignore` – never commit it!

### 4️⃣ Run the Front‑End Tagging Script
```bash
python add_contributor_and_tag.py
```
The script will:
- Add you (`@kunaaall`) as a collaborator on the repo.
- Add a **`frontend`** label (if it does not exist).
- Append a comment to every issue that is **tagged as front‑end** (or all issues if none are labelled) mentioning you, e.g.:
  > `@kunaaall – you are now assigned to this front‑end issue. Feel free to start working!`
- Print a short summary of actions performed.

## 📂 Repository Layout (quick reference)
```
shapeshifter/
├─ .github/               # Issue templates, workflows
├─ issues/                # CSV & scripts for bulk issue creation
│   ├─ create_all_issues.py
│   └─ add_contributor_and_tag.py   # <‑‑ this script
├─ docs/                  # Documentation folder (add your docs here)
│   └─ antigravity_frontend_guide.md   # <‑‑ you are reading it!
├─ src/                   # Source code (frontend lives under src/frontend/)
└─ README.md
```

## 🛠️ Working on a Front‑End Issue
1. **Open the issue** on GitHub – you’ll see a comment tagging you.
2. **Checkout a branch** for the issue:
   ```bash
   git checkout -b issue-<number>-frontend
   ```
3. **Make changes** in `src/frontend/…` using Antigravity’s editor.
4. **Run the dev server** (if the project uses Vite/Next.js, see the repo’s `README.md`).
5. **Commit & push**:
   ```bash
   git add .
   git commit -m "feat: implement <feature> for issue #<number>"
   git push origin HEAD
   ```
6. **Create a PR** on GitHub – reference the issue number (`#<number>`).
7. **Ask for review** – the CI pipeline will run automatically.

## 🐛 Bug Fixing Workflow
If you are assigned a bug (labelled `bug`), follow this process:

### 1. Reproduce the Issue
- Read the issue description carefully.
- Try to reproduce the bug in your local environment.
- If you can't reproduce it, comment on the issue asking for more details.

### 2. Create a Fix Branch
```bash
git checkout -b fix/issue-<number>-short-desc
```

### 3. Implement the Fix
- Locate the code causing the issue.
- Write a test case that fails (if possible) to confirm the bug.
- Apply your fix.
- Verify the test case now passes.

### 4. Verify & Push
- Run the full test suite to ensure no regressions.
- Push your changes:
  ```bash
  git push origin fix/issue-<number>-short-desc
  ```

### 5. Submit PR
- Create a Pull Request.
- In the description, use "Fixes #<number>" to automatically close the issue when merged.
- Request a review from @karan100010.

## 🐞 Debugging in Antigravity
- **Logs**: Check the terminal output for error stack traces.
- **Browser DevTools**: Use F12 to inspect console errors and network requests.
- **Breakpoints**: You can add `debugger;` in your JS/TS code to pause execution in the browser.

## ✅ Verification
After running the script you should see:
- `@kunaaall` listed under **Collaborators** in the repo settings.
- A new **`frontend`** label in the GitHub issue label list.
- A comment on each front‑end issue mentioning `@kunaaall`.

## 📖 Further Reading
- Antigravity IDE docs: https://github.com/karan100010/shapeshifter#antigravity-ide
- GitHub Collaboration guide: https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/adding-collaborators-to-a-personal-repository
- Front‑end contribution best practices (coding style, linting, testing) – see the `CONTRIBUTING.md` in the repo.

---
*Happy coding, @kunaaall!*
