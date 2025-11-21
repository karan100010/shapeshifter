# Create GitHub Issues for Frontend Tasks
# Make sure you've authenticated with: gh auth login

$repo = "karan100010/shapeshifter"

Write-Host "Creating frontend issues on GitHub..." -ForegroundColor Green
Write-Host "Repository: $repo`n" -ForegroundColor Cyan

# Issue #39: Document Upload Interface
Write-Host "Creating Issue #39: Document Upload Interface..." -ForegroundColor Yellow
$body39 = @"
Create a document upload interface for users to add documents to the RAG system with drag-and-drop support and progress tracking.

### Acceptance Criteria
- [ ] Drag-and-drop file upload
- [ ] Multiple file selection
- [ ] File type validation (PDF, TXT, DOCX, MD)
- [ ] Upload progress indicators
- [ ] File preview before upload
- [ ] Batch upload support
- [ ] Upload status notifications
- [ ] Error handling and retry

### Technical Requirements
- File upload component with drag-and-drop
- Progress bars for upload status
- File type icons and previews
- Integration with backend `/index` endpoint
- Maximum file size validation (e.g., 10MB)
- Responsive design

### Dependencies
- #1 API Gateway Setup (for upload endpoint)
- #23 Chunker Agent (backend processing)

### Implementation Notes
- Use Next.js file upload patterns
- Consider using react-dropzone for drag-and-drop
- Implement chunked uploads for large files
- Add file type icons for better UX
"@

gh issue create --repo $repo --title "Implement Document Upload Interface" --body $body39 --label "frontend,priority-high,enhancement" --assignee "kunaaalll"

# Issue #40: Document Management Dashboard
Write-Host "Creating Issue #40: Document Management Dashboard..." -ForegroundColor Yellow
$body40 = @"
Build a comprehensive dashboard for viewing, searching, and managing uploaded documents with full CRUD operations.

### Acceptance Criteria
- [ ] Document list view with pagination
- [ ] Search and filter functionality
- [ ] Document metadata display (name, size, upload date, status)
- [ ] Document preview modal
- [ ] Delete document functionality
- [ ] Bulk operations (delete multiple)
- [ ] Sort by date, name, size
- [ ] Document statistics widget

### Technical Requirements
- Table/grid view for documents
- Search bar with real-time filtering
- Modal component for document preview
- Confirmation dialogs for destructive actions
- Integration with backend metadata API
- Pagination component

### Dependencies
- #8 PostgreSQL Metadata Store
- #39 Document Upload Interface
"@

gh issue create --repo $repo --title "Build Document Management Dashboard" --body $body40 --label "frontend,priority-medium,enhancement" --assignee "kunaaalll"

# Issue #41: Query Analytics Dashboard
Write-Host "Creating Issue #41: Query Analytics Dashboard..." -ForegroundColor Yellow
$body41 = @"
Create an analytics dashboard showing query patterns, performance metrics, and usage statistics with interactive visualizations.

### Acceptance Criteria
- [ ] Query history view with details
- [ ] Performance metrics (latency, success rate)
- [ ] Popular queries visualization
- [ ] User activity charts
- [ ] Retrieval method comparison
- [ ] Time-series graphs
- [ ] Export functionality (CSV/JSON)
- [ ] Date range filtering

### Technical Requirements
- Chart library integration (Chart.js or Recharts)
- Real-time data updates
- Responsive charts and graphs
- Data export functionality
- Integration with metrics API
- Date range picker component

### Dependencies
- #5 Monitoring & Observability
- #27 Evaluator Agent
"@

gh issue create --repo $repo --title "Create Query Analytics Dashboard" --body $body41 --label "frontend,priority-medium,enhancement,analytics" --assignee "kunaaalll"

# Issue #42: Settings & Configuration UI
Write-Host "Creating Issue #42: Settings & Configuration UI..." -ForegroundColor Yellow
$body42 = @"
Build a comprehensive settings interface for configuring RAG system parameters and user preferences.

### Acceptance Criteria
- [ ] User profile management
- [ ] API key management with generation
- [ ] Retrieval settings (top-k, fusion weights)
- [ ] Model selection (embedding model, LLM)
- [ ] Theme customization (dark/light mode)
- [ ] Notification preferences
- [ ] Export/import settings
- [ ] Settings validation and error handling

### Technical Requirements
- Form components with validation
- Toggle switches, sliders, dropdowns
- Settings persistence (localStorage + backend sync)
- Real-time preview of changes
- Reset to defaults functionality
- Organized into sections/tabs

### Dependencies
- #34 Configuration Management
"@

gh issue create --repo $repo --title "Implement Settings & Configuration Interface" --body $body42 --label "frontend,priority-low,enhancement" --assignee "kunaaalll"

# Issue #43: Knowledge Graph Visualization
Write-Host "Creating Issue #43: Knowledge Graph Visualization..." -ForegroundColor Yellow
$body43 = @"
Create an interactive visualization of the knowledge graph for exploring entities, relationships, and communities.

### Acceptance Criteria
- [ ] Interactive graph visualization
- [ ] Node and edge filtering
- [ ] Entity detail panels
- [ ] Relationship exploration
- [ ] Search within graph
- [ ] Zoom and pan controls
- [ ] Community highlighting (color-coded)
- [ ] Export graph view (PNG/SVG)

### Technical Requirements
- Graph visualization library (D3.js, Cytoscape.js, or vis.js)
- Force-directed layout algorithm
- Node clustering by community
- Interactive tooltips for entities
- Performance optimization for large graphs (1000+ nodes)
- Lazy loading for large graphs

### Dependencies
- #7 Neo4j Graph Database
- #13 Knowledge Graph Construction
- #15 Community Detection
"@

gh issue create --repo $repo --title "Build Interactive Knowledge Graph Visualization" --body $body43 --label "frontend,graph-rag,priority-low,enhancement,visualization" --assignee "kunaaalll"

# Issue #44: Response Quality Feedback UI
Write-Host "Creating Issue #44: Response Quality Feedback UI..." -ForegroundColor Yellow
$body44 = @"
Implement user feedback mechanism for rating response quality, reporting issues, and improving the RAG system.

### Acceptance Criteria
- [ ] Thumbs up/down buttons on responses
- [ ] Detailed feedback form
- [ ] Issue reporting functionality
- [ ] Feedback history view
- [ ] Response regeneration button
- [ ] Citation-specific feedback
- [ ] Feedback analytics display
- [ ] Thank you confirmation message

### Technical Requirements
- Feedback buttons on each AI response
- Modal for detailed feedback submission
- Feedback submission to backend API
- Local feedback state management
- Analytics integration for tracking
- Feedback history page

### Dependencies
- #38 RAG Chatbot UI (completed)
- #27 Evaluator Agent
"@

gh issue create --repo $repo --title "Implement Response Quality Feedback System" --body $body44 --label "frontend,priority-medium,enhancement,user-feedback" --assignee "kunaaalll"

# Issue #45: Authentication & User Management UI
Write-Host "Creating Issue #45: Authentication & User Management UI..." -ForegroundColor Yellow
$body45 = @"
Build comprehensive authentication and user management interfaces with OAuth support and role-based access control.

### Acceptance Criteria
- [ ] Login page with form validation
- [ ] Registration page
- [ ] Password reset flow (email-based)
- [ ] User profile page
- [ ] Session management
- [ ] OAuth integration (Google, GitHub)
- [ ] Multi-factor authentication (optional)
- [ ] Role-based access control UI

### Technical Requirements
- Form validation (email, password strength)
- JWT token management
- Secure password handling (no plaintext)
- OAuth providers integration
- Session persistence across page reloads
- Protected routes (redirect to login)
- Remember me functionality

### Dependencies
- #1 API Gateway Setup (authentication endpoints)
"@

gh issue create --repo $repo --title "Build Authentication & User Management Interface" --body $body45 --label "frontend,infrastructure,priority-high,enhancement,security" --assignee "kunaaalll"

Write-Host "`n✅ All frontend issues created successfully!" -ForegroundColor Green
Write-Host "`nNext: Check for completed issues to close..." -ForegroundColor Cyan

# List all issues to find any completed ones
Write-Host "`nListing all issues..." -ForegroundColor Yellow
gh issue list --repo $repo --state all --limit 50

Write-Host "`n📝 Note: If you find a 'RAG Chatbot UI' or 'Frontend Dashboard' issue, close it manually with:" -ForegroundColor Yellow
Write-Host "gh issue close <issue-number> --repo $repo --comment 'Completed - see walkthrough.md'" -ForegroundColor Cyan
