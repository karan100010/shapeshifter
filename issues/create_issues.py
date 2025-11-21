#!/usr/bin/env python3
"""
GitHub Issue Creator for RAG Enhanced Architecture

This script creates GitHub issues programmatically using the GitHub API.
Requires: pip install PyGithub python-dotenv

Usage:
    1. Create a GitHub Personal Access Token with 'repo' scope
    2. Set environment variable: GITHUB_TOKEN=your_token_here
    3. Set environment variable: GITHUB_REPO=username/repository
    4. Run: python create_issues.py
"""

import os
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')  # Format: "username/repository"

if not GITHUB_TOKEN or not GITHUB_REPO:
    print("Error: Please set GITHUB_TOKEN and GITHUB_REPO environment variables")
    print("Example:")
    print("  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx")
    print("  export GITHUB_REPO=username/shapeshifter")
    exit(1)

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# Define all issues
issues_data = [
    # Category 1: Core Infrastructure
    {
        "title": "API Gateway Setup",
        "body": """Implement a production-ready API Gateway with authentication, rate limiting, and load balancing capabilities.

**Acceptance Criteria:**
- [ ] JWT-based authentication implemented
- [ ] Rate limiting per user/API key
- [ ] Load balancing across multiple backend instances
- [ ] Request/response logging
- [ ] API versioning support
- [ ] CORS configuration
- [ ] Health check endpoints

**Technical Requirements:**
- Framework: FastAPI or Flask with extensions
- Authentication: JWT tokens with refresh mechanism
- Rate Limiting: Redis-based token bucket algorithm
- Load Balancing: Nginx or built-in round-robin

**Dependencies:**
- Redis for rate limiting state
- PostgreSQL for user/API key management""",
        "labels": ["infrastructure", "priority-high"]
    },
    {
        "title": "Event Bus Implementation",
        "body": """Set up a message broker (RabbitMQ or Kafka) for asynchronous agent communication and event-driven workflows.

**Acceptance Criteria:**
- [ ] Message broker deployed and configured
- [ ] Topic/queue structure defined
- [ ] Publisher/subscriber pattern implemented
- [ ] Dead letter queue for failed messages
- [ ] Message persistence enabled
- [ ] Monitoring and metrics collection

**Technical Requirements:**
- Technology: RabbitMQ (recommended) or Kafka
- Message Format: JSON with schema validation
- Delivery Guarantee: At-least-once delivery
- Retry Logic: Exponential backoff""",
        "labels": ["infrastructure", "priority-high"]
    },
    {
        "title": "Control Plane Orchestrator",
        "body": """Implement the event-driven orchestrator for managing agent lifecycle and workflow execution with checkpointing and recovery.

**Acceptance Criteria:**
- [ ] Workflow state management (PENDING, RUNNING, COMPLETED, FAILED, PAUSED)
- [ ] Agent registry and discovery
- [ ] Checkpoint creation and recovery
- [ ] Workflow progress tracking
- [ ] Error handling and retry logic
- [ ] Workflow cancellation support

**Technical Requirements:**
- Language: Python with asyncio
- State Storage: PostgreSQL
- Event Bus Integration: Subscribe to agent completion/failure events
- Workflow Types: Indexing, Query, Optimization

**Dependencies:**
- Event Bus Implementation
- State Store Setup""",
        "labels": ["infrastructure", "agent", "priority-high"]
    },
    {
        "title": "State Store Setup",
        "body": """Configure PostgreSQL database for workflow state, metadata, and system configuration storage.

**Acceptance Criteria:**
- [ ] PostgreSQL instance deployed
- [ ] Database schema designed and created
- [ ] Connection pooling configured
- [ ] Backup and recovery procedures
- [ ] Migration scripts
- [ ] Performance indexes created

**Technical Requirements:**
- PostgreSQL Version: 14+
- ORM: SQLAlchemy
- Migration Tool: Alembic
- Connection Pool: pgbouncer or SQLAlchemy pool

**Schema Tables:**
- workflows, agents, users, api_keys, metrics""",
        "labels": ["storage", "infrastructure", "priority-high"]
    },
    {
        "title": "Monitoring & Observability",
        "body": """Implement comprehensive monitoring, logging, and tracing using Prometheus, Grafana, and Jaeger/OpenTelemetry.

**Acceptance Criteria:**
- [ ] Prometheus metrics collection
- [ ] Grafana dashboards for key metrics
- [ ] Distributed tracing with Jaeger
- [ ] Centralized logging
- [ ] Alerting rules configured
- [ ] Performance profiling

**Key Metrics:**
- Request latency (p50, p95, p99)
- Throughput (requests/sec)
- Error rates
- Agent execution times
- Database query performance
- Cache hit rates""",
        "labels": ["infrastructure", "deployment", "priority-medium"]
    },
    
    # Category 2: Storage Layer
    {
        "title": "Vector Database Setup",
        "body": """Deploy and configure a vector database (Milvus, Qdrant, or Weaviate) for embedding storage and similarity search.

**Acceptance Criteria:**
- [ ] Vector database deployed
- [ ] Collection/index created with appropriate schema
- [ ] Similarity search configured (cosine, dot product, L2)
- [ ] Indexing strategy optimized (IVF, HNSW)
- [ ] Batch insertion support
- [ ] Filtering capabilities

**Technical Requirements:**
- Recommended: Milvus or Qdrant
- Embedding Dimension: 768 or 1536
- Index Type: HNSW for speed
- Distance Metric: Cosine similarity""",
        "labels": ["storage", "priority-high"]
    },
    {
        "title": "Neo4j Graph Database",
        "body": """Set up Neo4j graph database with schema design, constraints, and indexes for knowledge graph storage.

**Acceptance Criteria:**
- [ ] Neo4j instance deployed
- [ ] Graph schema implemented
- [ ] Constraints and indexes created
- [ ] Full-text search indexes configured
- [ ] Graph Data Science library installed
- [ ] Backup procedures established

**Schema Components:**
- Node Types: Document, Chunk, Entity, Concept
- Relationships: CONTAINS, MENTIONS, RELATED_TO, etc.
- Constraints: Unique IDs for all node types""",
        "labels": ["storage", "graph-rag", "priority-high"]
    },
    {
        "title": "PostgreSQL Metadata Store",
        "body": """Configure PostgreSQL for metadata storage including document metadata, user data, and system configuration.

**Acceptance Criteria:**
- [ ] Database instance configured
- [ ] Metadata schema designed
- [ ] Indexes for common queries
- [ ] JSON/JSONB support for flexible metadata
- [ ] Full-text search capabilities
- [ ] Partitioning for large tables""",
        "labels": ["storage", "priority-high"]
    },
    {
        "title": "Redis Cache Layer",
        "body": """Implement Redis caching for frequently accessed data, rate limiting state, and session management.

**Acceptance Criteria:**
- [ ] Redis instance deployed
- [ ] Cache eviction policy configured (LRU)
- [ ] TTL strategies for different data types
- [ ] Cache invalidation logic
- [ ] Pub/sub for cache updates
- [ ] Persistence configuration

**Cache Use Cases:**
- Query results caching
- Embedding caching
- Rate limiting counters
- Session storage""",
        "labels": ["storage", "infrastructure", "priority-medium"]
    },
    
    # Add remaining issues here (truncated for brevity)
    # You would continue with all 37 issues following the same pattern
]

def create_labels(repo):
    """Create labels if they don't exist"""
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
    
    existing_labels = {label.name for label in repo.get_labels()}
    
    for label_name, color in labels_config.items():
        if label_name not in existing_labels:
            try:
                repo.create_label(label_name, color)
                print(f"✓ Created label: {label_name}")
            except Exception as e:
                print(f"✗ Failed to create label {label_name}: {e}")

def create_issues(repo, issues_data, dry_run=False):
    """Create GitHub issues"""
    print(f"\n{'DRY RUN: ' if dry_run else ''}Creating {len(issues_data)} issues...\n")
    
    for idx, issue_data in enumerate(issues_data, 1):
        title = issue_data["title"]
        body = issue_data["body"]
        labels = issue_data.get("labels", [])
        
        if dry_run:
            print(f"{idx}. [{', '.join(labels)}] {title}")
        else:
            try:
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=labels
                )
                print(f"✓ Created issue #{issue.number}: {title}")
            except Exception as e:
                print(f"✗ Failed to create issue '{title}': {e}")

def main():
    print(f"Repository: {GITHUB_REPO}")
    print(f"Authenticated as: {g.get_user().login}")
    
    # Ask for confirmation
    response = input("\nDo you want to create labels first? (y/n): ")
    if response.lower() == 'y':
        create_labels(repo)
    
    # Dry run option
    response = input("\nDo you want to do a dry run first? (y/n): ")
    if response.lower() == 'y':
        create_issues(repo, issues_data, dry_run=True)
        response = input("\nProceed with actual creation? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Create issues
    create_issues(repo, issues_data, dry_run=False)
    print("\n✓ Done!")

if __name__ == "__main__":
    main()
