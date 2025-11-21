# GitHub Issues Creation Guide

## Repository
**URL:** https://github.com/karan100010/shapeshifter

---

## Option 1: Install GitHub CLI (Recommended)

### Install GitHub CLI
```powershell
# Using winget (Windows Package Manager)
winget install --id GitHub.cli

# Or download from: https://cli.github.com/
```

### Authenticate
```powershell
gh auth login
```

### Create Issues Using CLI

After installing and authenticating, run these commands:

```powershell
# Navigate to repo
cd "c:\Users\KunalJoshi\OneDrive - Expense On Demand\Desktop\Shapeshifter\shapeshifter"

# Create Issue #39: Document Upload Interface
gh issue create --title "Implement Document Upload Interface" --body-file "issues/issue_39_body.md" --label "frontend,priority-high,enhancement" --assignee "kunaaalll"

# Create Issue #40: Document Management Dashboard
gh issue create --title "Build Document Management Dashboard" --body-file "issues/issue_40_body.md" --label "frontend,priority-medium,enhancement" --assignee "kunaaalll"

# Create Issue #41: Query Analytics Dashboard
gh issue create --title "Create Query Analytics Dashboard" --body-file "issues/issue_41_body.md" --label "frontend,priority-medium,enhancement,analytics" --assignee "kunaaalll"

# Create Issue #42: Settings & Configuration UI
gh issue create --title "Implement Settings & Configuration Interface" --body-file "issues/issue_42_body.md" --label "frontend,priority-low,enhancement" --assignee "kunaaalll"

# Create Issue #43: Knowledge Graph Visualization
gh issue create --title "Build Interactive Knowledge Graph Visualization" --body-file "issues/issue_43_body.md" --label "frontend,graph-rag,priority-low,enhancement,visualization" --assignee "kunaaalll"

# Create Issue #44: Response Quality Feedback UI
gh issue create --title "Implement Response Quality Feedback System" --body-file "issues/issue_44_body.md" --label "frontend,priority-medium,enhancement,user-feedback" --assignee "kunaaalll"

# Create Issue #45: Authentication & User Management UI
gh issue create --title "Build Authentication & User Management Interface" --body-file "issues/issue_45_body.md" --label "frontend,infrastructure,priority-high,enhancement,security" --assignee "kunaaalll"

# Close Issue #38 (RAG Chatbot UI - Completed)
# First, find the issue number if it exists
gh issue list --label "frontend" --state "all"

# If issue #38 exists, close it with a comment
gh issue close 38 --comment "✅ Completed! RAG Chatbot UI has been fully implemented with all features:
- Chat interface with message display
- Sidebar with chat history  
- Chat switching functionality
- New chat creation
- Query suggestions
- Citations display
- Copy-to-clipboard
- Typing indicators
- Message persistence
- Responsive design
- 41 unit tests (all passing)
- Browser verification complete

See walkthrough.md for full details."
```

---

## Option 2: Manual Creation via GitHub Web Interface

### Step 1: Go to Issues Page
Navigate to: https://github.com/karan100010/shapeshifter/issues

### Step 2: Create Labels (if they don't exist)

Go to: https://github.com/karan100010/shapeshifter/labels

Create these labels if missing:
- `frontend` (color: #0366d6)
- `priority-high` (color: #d73a4a)
- `priority-medium` (color: #fbca04)
- `priority-low` (color: #0e8a16)
- `enhancement` (color: #a2eeef)
- `analytics` (color: #d4c5f9)
- `visualization` (color: #5319e7)
- `user-feedback` (color: #c5def5)
- `security` (color: #ee0701)
- `graph-rag` (color: #1d76db)

### Step 3: Create Each Issue

Click "New Issue" and use the content from `frontend_issues_github.md`:

#### Issue #39: Document Upload Interface
- **Title:** Implement Document Upload Interface
- **Description:** Copy from `frontend_issues_github.md` (Issue #39 section)
- **Labels:** frontend, priority-high, enhancement
- **Assignee:** kunaaalll

#### Issue #40: Document Management Dashboard
- **Title:** Build Document Management Dashboard
- **Description:** Copy from `frontend_issues_github.md` (Issue #40 section)
- **Labels:** frontend, priority-medium, enhancement
- **Assignee:** kunaaalll

#### Issue #41: Query Analytics Dashboard
- **Title:** Create Query Analytics Dashboard
- **Description:** Copy from `frontend_issues_github.md` (Issue #41 section)
- **Labels:** frontend, priority-medium, enhancement, analytics
- **Assignee:** kunaaalll

#### Issue #42: Settings & Configuration UI
- **Title:** Implement Settings & Configuration Interface
- **Description:** Copy from `frontend_issues_github.md` (Issue #42 section)
- **Labels:** frontend, priority-low, enhancement
- **Assignee:** kunaaalll

#### Issue #43: Knowledge Graph Visualization
- **Title:** Build Interactive Knowledge Graph Visualization
- **Description:** Copy from `frontend_issues_github.md` (Issue #43 section)
- **Labels:** frontend, graph-rag, priority-low, enhancement, visualization
- **Assignee:** kunaaalll

#### Issue #44: Response Quality Feedback UI
- **Title:** Implement Response Quality Feedback System
- **Description:** Copy from `frontend_issues_github.md` (Issue #44 section)
- **Labels:** frontend, priority-medium, enhancement, user-feedback
- **Assignee:** kunaaalll

#### Issue #45: Authentication & User Management UI
- **Title:** Build Authentication & User Management Interface
- **Description:** Copy from `frontend_issues_github.md` (Issue #45 section)
- **Labels:** frontend, infrastructure, priority-high, enhancement, security
- **Assignee:** kunaaalll

### Step 4: Close Completed Issue

If there's an existing issue for "RAG Chatbot UI" or "Frontend Dashboard Implementation":
1. Find the issue number
2. Add a comment with completion details
3. Click "Close issue"

**Completion Comment:**
```
✅ Completed! RAG Chatbot UI has been fully implemented with all features:

**Implemented Features:**
- ✅ Chat interface with message display
- ✅ Sidebar with chat history  
- ✅ Chat switching functionality
- ✅ New chat creation
- ✅ Query suggestions
- ✅ Citations display
- ✅ Copy-to-clipboard
- ✅ Typing indicators
- ✅ Message persistence
- ✅ Responsive design

**Testing:**
- ✅ 41 unit tests (all passing)
- ✅ Browser verification complete

**Tech Stack:**
- Next.js 16.0.3
- React 19
- TypeScript
- CSS Modules
- Jest + React Testing Library

See `walkthrough.md` in the artifacts directory for full implementation details.
```

---

## Summary

**New Issues to Create:** 7 issues (#39-#45)
**Issues to Close:** 1 issue (RAG Chatbot UI - if it exists)

**Priority Order:**
1. Issue #45: Authentication & User Management (HIGH)
2. Issue #39: Document Upload Interface (HIGH)
3. Issue #41: Query Analytics Dashboard (MEDIUM)
4. Issue #44: Response Quality Feedback (MEDIUM)
5. Issue #40: Document Management Dashboard (MEDIUM)
6. Issue #42: Settings & Configuration (LOW)
7. Issue #43: Knowledge Graph Visualization (LOW)
