# Shapeshifter RAG - Complete Testing Guide

## Overview

This guide provides comprehensive testing instructions for the Shapeshifter RAG Enhanced Architecture, covering:
- Backend API Testing
- Frontend UI Testing  
- Full-Stack Integration Testing
- Docker-based Testing Environment

## System Architecture

```
Frontend (Next.js) - Branch: Dizzyommits - Port: 3000
           |
           v HTTP/REST API
Backend (FastAPI) - Branch: karan100010 - Port: 8080
           |
    Databases (Neo4j, Qdrant, PostgreSQL, Redis)
```

## Prerequisites

### Required Software
- Docker Desktop (running)
- Python 3.10+
- Node.js 18+ (for frontend development)
- Git

### Environment Setup
1. Clone repository
2. Create `.env` file with database configurations
3. Install Docker and start Docker Desktop

## Backend Testing

### 1. Backend Docker Build Test
```bash
python test_docker_build.py
```

### 2. Start Backend Services
```bash
docker-compose up -d
```

### 3. Backend API Health Check
```bash
curl http://localhost:8080/health
```

### 4. Backend API Documentation
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### 5. Testing Scenarios

**Create Workflow:**
```bash
curl -X POST http://localhost:8080/workflows \
  -H "Content-Type: application/json" \
  -d '{"workflow_type": "indexing", "inputs": {"document_text": "Test"}}'
```

**Check Workflow Status:**
```bash
curl http://localhost:8080/workflows/{workflow_id}
```

## Frontend Testing (Dizzyommits Branch)

### 1. Frontend Setup
```bash
git checkout Dizzyommits
cd src/frontend
npm install
```

### 2. Development Mode
```bash
npm run dev
# Open: http://localhost:3000
```

### 3. Frontend Docker Build
```bash
cd src/frontend
docker build -t shapeshifter-frontend:latest .
docker run -p 3000:3000 shapeshifter-frontend:latest
```

### 4. Frontend Tests
```bash
npm test
npm run lint
```

## Full-Stack Integration

Use provided script:
```bash
python run_fullstack.py
```

## Ports Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 8080 | http://localhost:8080 |
| Neo4j | 7474, 7687 | http://localhost:7474 |
| Qdrant | 6333 | http://localhost:6333 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |

## Troubleshooting

### Backend Issues
```bash
docker-compose logs backend
docker-compose restart backend
```

### Frontend Issues
```bash
cd src/frontend
rm -rf node_modules .next
npm install
```

See full guide in documentation for detailed scenarios.
