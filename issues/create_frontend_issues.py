#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Frontend Issues Creator for ShapeShifter
Creates frontend-specific GitHub issues using a provided PAT token and closes completed chatbot UI issue.
"""

import sys
import os
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

if not GITHUB_TOKEN or not GITHUB_REPO:
    print("Error: Please set GITHUB_TOKEN and GITHUB_REPO environment variables")
    sys.exit(1)

# Initialize GitHub client
try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
except Exception as e:
    print(f"Error: Failed to authenticate or access repository: {e}")
    sys.exit(1)

# Frontend issue definitions (title, body, labels, assignees)
frontend_issues = [
    {
        "title": "Implement Document Upload Interface",
        "body": "Create a document upload interface for users to add documents to the RAG system with drag-and-drop support and progress tracking.\n\n### Acceptance Criteria\n- [ ] Drag-and-drop file upload\n- [ ] Multiple file selection\n- [ ] File type validation (PDF, TXT, DOCX, MD)\n- [ ] Upload progress indicators\n- [ ] File preview before upload\n- [ ] Batch upload support\n- [ ] Upload status notifications\n- [ ] Error handling and retry\n\n### Technical Requirements\n- File upload component with drag-and-drop\n- Progress bars for upload status\n- File type icons and previews\n- Integration with backend `/index` endpoint\n- Maximum file size validation (e.g., 10MB)\n- Responsive design\n\n### Dependencies\n- #1 API Gateway Setup (for upload endpoint)\n- #23 Chunker Agent (backend processing)",
        "labels": ["frontend", "priority-high", "enhancement"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Build Document Management Dashboard",
        "body": "Build a comprehensive dashboard for viewing, searching, and managing uploaded documents with full CRUD operations.\n\n### Acceptance Criteria\n- [ ] Document list view with pagination\n- [ ] Search and filter functionality\n- [ ] Document metadata display (name, size, upload date, status)\n- [ ] Document preview modal\n- [ ] Delete document functionality\n- [ ] Bulk operations (delete multiple)\n- [ ] Sort by date, name, size\n- [ ] Document statistics widget\n\n### Technical Requirements\n- Table/grid view for documents\n- Search bar with real-time filtering\n- Modal component for document preview\n- Confirmation dialogs for destructive actions\n- Integration with backend metadata API\n- Pagination component\n\n### Dependencies\n- #8 PostgreSQL Metadata Store\n- Document Upload Interface",
        "labels": ["frontend", "priority-medium", "enhancement"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Create Query Analytics Dashboard",
        "body": "Create an analytics dashboard showing query patterns, performance metrics, and usage statistics with interactive visualizations.\n\n### Acceptance Criteria\n- [ ] Query history view with details\n- [ ] Performance metrics (latency, success rate)\n- [ ] Popular queries visualization\n- [ ] User activity charts\n- [ ] Retrieval method comparison\n- [ ] Time-series graphs\n- [ ] Export functionality (CSV/JSON)\n- [ ] Date range filtering\n\n### Technical Requirements\n- Chart library integration (Chart.js or Recharts)\n- Real-time data updates\n- Responsive charts and graphs\n- Data export functionality\n- Integration with metrics API\n- Date range picker component\n\n### Dependencies\n- #5 Monitoring & Observability\n- #27 Evaluator Agent",
        "labels": ["frontend", "priority-medium", "enhancement", "analytics"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Implement Settings & Configuration Interface",
        "body": "Build a comprehensive settings interface for configuring RAG system parameters and user preferences.\n\n### Acceptance Criteria\n- [ ] User profile management\n- [ ] API key management with generation\n- [ ] Retrieval settings (top-k, fusion weights)\n- [ ] Model selection (embedding model, LLM)\n- [ ] Theme customization (dark/light mode)\n- [ ] Notification preferences\n- [ ] Export/import settings\n- [ ] Settings validation and error handling\n\n### Technical Requirements\n- Form components with validation\n- Toggle switches, sliders, dropdowns\n- Settings persistence (localStorage + backend sync)\n- Real-time preview of changes\n- Reset to defaults functionality\n- Organized into sections/tabs\n\n### Dependencies\n- #34 Configuration Management",
        "labels": ["frontend", "priority-low", "enhancement"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Build Interactive Knowledge Graph Visualization",
        "body": "Create an interactive visualization of the knowledge graph for exploring entities, relationships, and communities.\n\n### Acceptance Criteria\n- [ ] Interactive graph visualization\n- [ ] Node and edge filtering\n- [ ] Entity detail panels\n- [ ] Relationship exploration\n- [ ] Search within graph\n- [ ] Zoom and pan controls\n- [ ] Community highlighting (color-coded)\n- [ ] Export graph view (PNG/SVG)\n\n### Technical Requirements\n- Graph visualization library (D3.js, Cytoscape.js, or vis.js)\n- Force-directed layout algorithm\n- Node clustering by community\n- Interactive tooltips for entities\n- Performance optimization for large graphs (1000+ nodes)\n- Lazy loading for large graphs\n\n### Dependencies\n- #7 Neo4j Graph Database\n- #13 Knowledge Graph Construction\n- #15 Community Detection",
        "labels": ["frontend", "graph-rag", "priority-low", "enhancement", "visualization"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Implement Response Quality Feedback System",
        "body": "Implement user feedback mechanism for rating response quality, reporting issues, and improving the RAG system.\n\n### Acceptance Criteria\n- [ ] Thumbs up/down buttons on responses\n- [ ] Detailed feedback form\n- [ ] Issue reporting functionality\n- [ ] Feedback history view\n- [ ] Response regeneration button\n- [ ] Citation-specific feedback\n- [ ] Feedback analytics display\n- [ ] Thank you confirmation message\n\n### Technical Requirements\n- Feedback buttons on each AI response\n- Modal for detailed feedback submission\n- Feedback submission to backend API\n- Local feedback state management\n- Analytics integration for tracking\n- Feedback history page\n\n### Dependencies\n- RAG Chatbot UI (completed)\n- #27 Evaluator Agent",
        "labels": ["frontend", "priority-medium", "enhancement", "user-feedback"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Build Authentication & User Management Interface",
        "body": "Build comprehensive authentication and user management interfaces with OAuth support and role-based access control.\n\n### Acceptance Criteria\n- [ ] Login page with form validation\n- [ ] Registration page\n- [ ] Password reset flow (email-based)\n- [ ] User profile page\n- [ ] Session management\n- [ ] OAuth integration (Google, GitHub)\n- [ ] Multi-factor authentication (optional)\n- [ ] Role-based access control UI\n\n### Technical Requirements\n- Form validation (email, password strength)\n- JWT token management\n- Secure password handling (no plaintext)\n- OAuth providers integration\n- Session persistence across page reloads\n- Protected routes (redirect to login)\n- Remember me functionality\n\n### Dependencies\n- #1 API Gateway Setup (authentication endpoints)",
        "labels": ["frontend", "infrastructure", "priority-high", "enhancement", "security"],
        "assignees": ["kunaaalll"]
    }
]

# Completed issues to be created and immediately closed
completed_issues = [
    {
        "title": "Implement RAG Chatbot UI",
        "body": "Develop the core chat interface for the RAG system.\n\n### Implemented Features\n- Chat interface with message display (User/AI bubbles)\n- Sidebar with chat history and new chat creation\n- Chat switching functionality\n- Query suggestions (chips)\n- Citations display with sources\n- Copy-to-clipboard functionality\n- Typing indicators\n- Message persistence (local state/mock)\n- Responsive design\n\n**Files:** `ChatContainer.tsx`, `ChatInput.tsx`, `ChatSidebar.tsx`, `Message.tsx`, `page.tsx`",
        "labels": ["frontend", "enhancement", "ui"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Create Dashboard Layout & Navigation",
        "body": "Implement the main application layout and navigation structure.\n\n### Implemented Features\n- Responsive sidebar navigation\n- Header with user profile placeholder\n- Main content area structure\n- Theme consistency (CSS modules)\n\n**Files:** `Sidebar.tsx`, `Header.tsx`, `layout.tsx`, `globals.css`",
        "labels": ["frontend", "enhancement", "ui"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Build Statistics Widgets",
        "body": "Create reusable widget components for displaying system metrics.\n\n### Implemented Features\n- Stat cards with titles, values, and trends\n- Visual indicators for positive/negative trends\n- Responsive grid layout support\n\n**Files:** `StatsWidget.tsx`",
        "labels": ["frontend", "enhancement", "ui"],
        "assignees": ["kunaaalll"]
    },
    {
        "title": "Setup Frontend Testing Infrastructure",
        "body": "Configure testing framework and create initial test suite.\n\n### Implemented Features\n- Jest and React Testing Library configuration\n- Unit tests for all core components (ChatContainer, ChatInput, Sidebar, etc.)\n- 41 passing tests\n\n**Files:** `jest.config.ts`, `__tests__/*.test.tsx`",
        "labels": ["frontend", "testing", "infrastructure"],
        "assignees": ["kunaaalll"]
    }
]

def ensure_labels(repo):
    label_defs = {
        "frontend": "0366d6",
        "priority-high": "d73a4a",
        "priority-medium": "fbca04",
        "priority-low": "0e8a16",
        "enhancement": "a2eeef",
        "analytics": "d4c5f9",
        "visualization": "5319e7",
        "user-feedback": "c5def5",
        "security": "ee0701",
        "infrastructure": "0052cc",
        "graph-rag": "1d76db"
    }
    existing = {l.name for l in repo.get_labels()}
    for name, color in label_defs.items():
        if name not in existing:
            try:
                repo.create_label(name, color)
                print(f"Created label: {name}")
            except Exception as e:
                print(f"Failed to create label {name}: {e}")

def create_frontend_issues(repo, issues):
    print(f"Creating {len(issues)} frontend issues...")
    created = []
    for issue in issues:
        try:
            gh_issue = repo.create_issue(
                title=issue["title"],
                body=issue["body"],
                labels=issue["labels"],
                assignees=issue["assignees"]
            )
            created.append(gh_issue.number)
            print(f"Created issue #{gh_issue.number}: {issue['title']}")
        except Exception as e:
            print(f"Failed to create issue '{issue['title']}': {e}")
    return created

def close_completed_chatbot_issue(repo):
    for issue in repo.get_issues(state='open'):
        if "chatbot ui" in issue.title.lower() or "rag chatbot" in issue.title.lower():
            comment = "Completed! RAG Chatbot UI has been fully implemented."
            try:
                issue.create_comment(comment)
                issue.edit(state='closed')
                print(f"Closed issue #{issue.number}: {issue.title}")
                return True
            except Exception as e:
                print(f"Failed to close issue #{issue.number}: {e}")
    return False

def create_and_close_completed_issues(repo, issues):
    print(f"Processing {len(issues)} completed issues...")
    for issue in issues:
        try:
            # Check if issue already exists
            exists = False
            for existing in repo.get_issues(state='all'):
                if issue["title"] == existing.title:
                    print(f"Issue '{issue['title']}' already exists (#{existing.number})")
                    exists = True
                    break
            
            if not exists:
                gh_issue = repo.create_issue(
                    title=issue["title"],
                    body=issue["body"],
                    labels=issue["labels"],
                    assignees=issue["assignees"]
                )
                print(f"Created issue #{gh_issue.number}: {issue['title']}")
                
                # Close the issue
                gh_issue.create_comment("✅ This work has been completed and verified.")
                gh_issue.edit(state='closed')
                print(f"Closed issue #{gh_issue.number}")
                
        except Exception as e:
            print(f"Failed to process issue '{issue['title']}': {e}")

def main():
    print(f"Repository: {GITHUB_REPO}")
    print(f"Authenticated as: {g.get_user().login}")
    ensure_labels(repo)
    
    # Create open frontend issues
    create_frontend_issues(repo, frontend_issues)
    
    # Create and close completed issues
    create_and_close_completed_issues(repo, completed_issues)
    
    # Close legacy chatbot issue if it exists
    close_completed_chatbot_issue(repo)
    print("Done!")

if __name__ == "__main__":
    main()
