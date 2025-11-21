# GitHub Issue Creation Setup Guide

## 🔑 Step 1: Create GitHub Personal Access Token

### **Create the Token:**

1. **Navigate to GitHub Token Settings:**
   - Go to: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token (Classic):**
   - Click **"Generate new token"** → **"Generate new token (classic)"**
   - **Note:** Give it a descriptive name (e.g., "ShapeShifter Issue Creator")
   - **Expiration:** Choose 90 days or custom duration
   - **Select scopes:** ✅ Check **`repo`** (Full control of private repositories)
     - This automatically includes all sub-scopes needed
   - Click **"Generate token"** at the bottom

3. **Copy Your Token:**
   - ⚠️ **CRITICAL:** Copy the token immediately - you won't see it again!
   - Format: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Store it securely (password manager recommended)

---

## ⚙️ Step 2: Configure Environment Variables

### **Option A: Using .env File (Recommended)**

1. Create a `.env` file in the `issues` directory:

```bash
# In c:\Users\karan\shapeshifter\issues\
```

2. Add the following content (replace with your actual values):

```env
GITHUB_TOKEN=ghp_your_actual_token_here
GITHUB_REPO=karan100010/shapeshifter
```

3. **Security:** Make sure `.env` is in your `.gitignore` to avoid committing secrets!

### **Option B: Using PowerShell Environment Variables**

```powershell
# Set for current session only
$env:GITHUB_TOKEN="ghp_your_actual_token_here"
$env:GITHUB_REPO="karan100010/shapeshifter"

# Or set permanently (user-level)
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_your_actual_token_here', 'User')
[System.Environment]::SetEnvironmentVariable('GITHUB_REPO', 'karan100010/shapeshifter', 'User')
```

---

## ✅ Step 3: Verify Setup

Run this test command to verify your token works:

```bash
cd c:\Users\karan\shapeshifter\issues
python -c "from github import Github; import os; from dotenv import load_dotenv; load_dotenv(); g = Github(os.getenv('GITHUB_TOKEN')); print(f'✓ Authenticated as: {g.get_user().login}'); repo = g.get_repo(os.getenv('GITHUB_REPO')); print(f'✓ Repository: {repo.full_name}')"
```

Expected output:
```
✓ Authenticated as: karan100010
✓ Repository: karan100010/shapeshifter
```

---

## 🚀 Step 4: Run the Script

### **Dry Run First (Recommended):**

```bash
cd c:\Users\karan\shapeshifter\issues
python create_issues.py
```

The script will:
1. Ask if you want to create labels first → Type `y`
2. Ask if you want a dry run → Type `y` (to preview)
3. Show all issues that would be created
4. Ask if you want to proceed → Type `y` to create issues

### **Direct Creation:**

If you're confident, you can skip the dry run:
- When asked "Do you want to do a dry run first?" → Type `n`

---

## 📊 What Will Be Created

The script currently has **8 issues** defined (truncated version). Based on your `all_issues.md`, you have **37 total issues** to create.

### **Current Issues in Script:**
1. ✅ API Gateway Setup
2. ✅ Event Bus Implementation
3. ✅ Control Plane Orchestrator
4. ✅ State Store Setup
5. ✅ Monitoring & Observability
6. ✅ Vector Database Setup
7. ✅ Neo4j Graph Database
8. ✅ PostgreSQL Metadata Store
9. ✅ Redis Cache Layer

### **Labels That Will Be Created:**
- `infrastructure` (blue)
- `storage` (dark blue)
- `graph-rag` (purple)
- `agent` (orange)
- `retrieval` (green)
- `deployment` (yellow)
- `testing` (light blue)
- `documentation` (blue)
- `priority-high` (red)
- `priority-medium` (yellow)
- `priority-low` (green)

---

## ⚠️ Important Notes

### **Token Security:**
- ✅ Never commit your token to Git
- ✅ Use `.env` file and add it to `.gitignore`
- ✅ Rotate tokens periodically
- ✅ Use minimum required permissions

### **Rate Limits:**
- GitHub API allows 5,000 requests/hour for authenticated users
- Creating 37 issues is well within limits
- The script includes error handling for rate limits

### **Repository Permissions:**
- Your token must have write access to the repository
- If using a personal repo, the `repo` scope is sufficient
- For organization repos, ensure you have appropriate permissions

---

## 🔧 Troubleshooting

### **Error: "Bad credentials"**
- Check that your token is correct and not expired
- Verify the token has `repo` scope
- Try regenerating the token

### **Error: "Not Found"**
- Verify repository name format: `username/repository`
- Check that the repository exists
- Ensure your token has access to the repository

### **Error: "Resource not accessible by integration"**
- Token lacks required permissions
- Regenerate token with `repo` scope

### **Import Error: "No module named 'github'"**
- Run: `pip install PyGithub python-dotenv`

---

## 📝 Next Steps

1. ✅ Dependencies installed (PyGithub, python-dotenv)
2. ⏳ Create GitHub Personal Access Token
3. ⏳ Configure environment variables
4. ⏳ Run verification test
5. ⏳ Execute script to create issues

**Note:** The current script only has 9 issues. You may want to add the remaining 28 issues from your `all_issues.md` file to the `issues_data` list in `create_issues.py`.
