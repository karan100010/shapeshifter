# Shapeshifter RAG - Tester Quick Start Guide

## Welcome, Tester! 👋

This guide will help you quickly set up and test the Shapeshifter RAG system (both backend and frontend).

## What You're Testing

**Shapeshifter** is a Retrieval-Augmented Generation (RAG) system with:
- **Backend**: FastAPI-based API with Graph RAG, vector search, and LLM integration
- **Frontend**: Next.js web application for document upload and querying
- **Databases**: Neo4j (graph), Qdrant (vectors), PostgreSQL, Redis

## Prerequisites

### Required (Must Have):
1. **Docker Desktop** - Install from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Python 3.10+** - For running test scripts
3. **Git** - For cloning the repository

### Optional (Nice to Have):
- **Node.js 18+** - If testing frontend in development mode
- **cURL** or **Postman** - For API testing

## Quick Start (5 Minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/karan100010/shapeshifter.git
cd shapeshifter
```

### Step 2: Start Docker Desktop
- Open Docker Desktop application
- Wait for it to fully start (Docker icon in system tray should be green)

### Step 3: Run Full Stack
```bash
python run_fullstack.py
```

This will:
- ✅ Check Docker is running
- ✅ Start all backend services
- ✅ Wait for services to be healthy
- ✅ Display access URLs

### Step 4: Access the System

**Frontend** (after switching to Dizzyommits branch):
```bash
git checkout Dizzyommits
cd src/frontend
npm install
npm run dev
```
Then open: http://localhost:3000

**Backend API Docs**: http://localhost:8080/docs

## Testing Checklist

### Backend Tests

- [ ] **Health Check**
  ```bash
  curl http://localhost:8080/health
  ```
  Expected: `{"status": "healthy"}`

- [ ] **API Documentation Loads**
  - Open http://localhost:8080/docs
  - Should see Swagger UI with all endpoints

- [ ] **Create Workflow**
  ```bash
  curl -X POST http://localhost:8080/workflows \
    -H "Content-Type: application/json" \
    -d '{"workflow_type": "indexing", "inputs": {"document_text": "This is a test document about AI."}}'
  ```
  Expected: Returns a workflow ID

- [ ] **Check Workflow Status**
  ```bash
  curl http://localhost:8080/workflows/{WORKFLOW_ID}
  ```
  Expected: Returns workflow status

- [ ] **Database Access**
  - Neo4j: http://localhost:7474 (login: neo4j / password)
  - Qdrant: http://localhost:6333/dashboard

### Frontend Tests (Dizzyommits Branch)

- [ ] **Page Loads**
  - Homepage: http://localhost:3000
  - Documents: http://localhost:3000/documents
  - Dashboard: http://localhost:3000/dashboard

- [ ] **Document Upload**
  1. Go to Documents page
  2. Upload a test file (PDF, TXT, MD)
  3. Verify upload succeeds

- [ ] **Chat Interface**
  1. Go to homepage
  2. Type a question
  3. Verify response appears

- [ ] **UI Responsiveness**
  - Test on different screen sizes
  - Check mobile view (resize browser)

### Integration Tests

- [ ] **End-to-End Flow**
  1. Upload document via frontend
  2. Wait for processing (check backend logs)
  3. Query the document content
  4. Verify results are correct

- [ ] **Error Handling**
  - Try uploading invalid file
  - Send malformed query
  - Verify error messages are shown

## Common Issues & Solutions

### Issue: "Docker is not running"
**Solution**: Start Docker Desktop and wait for it to fully initialize (green icon)

### Issue: "Port already in use"
**Solution**:
```bash
docker-compose down
# Wait 10 seconds
docker-compose up -d
```

### Issue: "Backend returns 500 error"
**Solution**: Check backend logs:
```bash
docker-compose logs backend
```

### Issue: "Frontend won't start"
**Solution**:
```bash
cd src/frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Issue: "Cannot connect to database"
**Solution**: Restart database services:
```bash
docker-compose restart neo4j qdrant postgres redis
```

## Viewing Logs

**All services**:
```bash
docker-compose logs -f
```

**Specific service**:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Last 100 lines**:
```bash
docker-compose logs --tail=100 backend
```

## Stopping the System

**Stop all services**:
```bash
docker-compose down
```

**Stop and remove all data**:
```bash
docker-compose down -v
```

## Test Reporting

### What to Report

When you find an issue, please include:
1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Screenshots** (if UI issue)
5. **Logs** (from `docker-compose logs`)
6. **Environment**:
   - OS (Windows/Mac/Linux)
   - Docker version (`docker --version`)
   - Browser (if frontend issue)

### Where to Report

Create an issue on GitHub: https://github.com/karan100010/shapeshifter/issues

Use this template:
```
## Bug Description
[What went wrong]

## Steps to Reproduce
1. ...
2. ...

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happened]

## Environment
- OS: [Windows 11 / Mac OS 14 / Ubuntu 22.04]
- Docker: [24.0.6]
- Browser: [Chrome 120 / Firefox 121]

## Logs
```
[Paste relevant logs here]
```

## Screenshots
[Attach screenshots]
```

## Advanced Testing

### Performance Testing

Test API response times:
```bash
# Install Apache Bench (if not installed)
# Windows: choco install apache-httpd
# Mac: brew install httpd
# Linux: apt-get install apache2-utils

# Run 100 requests with 10 concurrent
ab -n 100 -c 10 http://localhost:8080/health
```

### Load Testing

Test with multiple simultaneous uploads:
```bash
python performance_test.py
```

### Security Testing

- [ ] Test CORS headers
- [ ] Test authentication (if implemented)
- [ ] Test input validation
- [ ] Test file upload limits

## Useful Commands Reference

```bash
# Check status of all services
docker-compose ps

# Restart a specific service
docker-compose restart backend

# Rebuild after code changes
docker-compose up -d --build backend

# View resource usage
docker stats

# Clean everything and start fresh
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Export database for inspection
docker exec shapeshifter-postgres pg_dump -U postgres shapeshifter > backup.sql
```

## Questions?

- Check [TESTING_GUIDE.md](./TESTING_GUIDE.md) for detailed testing scenarios
- Check [docker_build_guide.md](./docker_build_guide.md) for Docker setup issues
- Create an issue on GitHub with questions

## System Ports

| Component | Port | URL |
|-----------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8080 | http://localhost:8080 |
| API Docs | 8080 | http://localhost:8080/docs |
| Neo4j Browser | 7474 | http://localhost:7474 |
| Qdrant Dashboard | 6333 | http://localhost:6333 |

## Happy Testing! 🚀

If you encounter issues, don't hesitate to ask for help or create a GitHub issue.
