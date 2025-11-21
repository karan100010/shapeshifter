# RAG Enhanced Architecture with Graph RAG

A production-ready Retrieval-Augmented Generation (RAG) system featuring hybrid retrieval (vector + sparse + graph), event-driven agent orchestration, and advanced knowledge graph integration using Neo4j.

## 🌟 Features

- **Hybrid Retrieval**: Combines vector embeddings, sparse retrieval (BM25), and graph-based retrieval for superior accuracy
- **Graph RAG Integration**: Leverages Neo4j for entity relationships, multi-hop reasoning, and contextual enrichment
- **Event-Driven Architecture**: Asynchronous agent communication via RabbitMQ/Kafka
- **Production-Ready**: Built for high availability, monitoring, security, and scalability
- **Self-Improving**: Continuous evaluation and optimization capabilities

## 🏗️ Architecture

### Technology Stack

**Storage Layer:**
- Vector DB: Milvus / Qdrant / Weaviate
- Graph DB: Neo4j Enterprise/Community
- Metadata DB: PostgreSQL
- Cache: Redis

**Processing Layer:**
- Embedding: sentence-transformers, OpenAI
- LLM: Local (Llama2, Mistral) or API (GPT-4, Claude)
- NLP: spaCy, NLTK for entity extraction
- Graph Processing: Neo4j Graph Data Science

**Infrastructure:**
- Orchestration: Docker Compose / Kubernetes
- Message Bus: RabbitMQ / Kafka
- Monitoring: Prometheus + Grafana
- Tracing: Jaeger / OpenTelemetry

### Core Components

1. **Control Plane Orchestrator** - Manages agent lifecycle and workflow execution
2. **Agent Ecosystem** - Specialized agents for analysis, retrieval, generation, and verification
3. **Graph RAG Pipeline** - Entity extraction, relationship mapping, and knowledge graph construction
4. **Hybrid Retrieval System** - Multi-strategy retrieval with intelligent fusion
5. **API Gateway** - Authentication, rate limiting, and load balancing

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Neo4j 5.0+
- PostgreSQL 14+
- Redis 7+

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shapeshifter.git
cd shapeshifter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start infrastructure services
docker-compose up -d

# Initialize databases
python scripts/init_databases.py

# Run the application
python main.py
```

## 📚 Documentation

- [Architecture Documentation](docs/architecture.md) - Detailed system architecture
- [API Documentation](docs/api.md) - REST API reference
- [Deployment Guide](docs/deployment.md) - Production deployment instructions
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute

## 🔧 Development

### Project Structure

```
shapeshifter/
├── agents/              # Agent implementations
├── control_plane/       # Orchestrator and workflow management
├── graph_rag/          # Graph RAG components
├── retrieval/          # Retrieval strategies
├── storage/            # Database adapters
├── api/                # API endpoints
├── config/             # Configuration files
├── tests/              # Test suites
└── docs/               # Documentation
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test suite
pytest tests/test_graph_rag.py
```

## 📊 Key Capabilities

### Graph RAG Features
- **Entity Extraction**: Advanced NER with spaCy and GLiNER
- **Relationship Extraction**: Dependency parsing and OpenIE
- **Multi-Hop Reasoning**: Graph path traversal for complex queries
- **Community Detection**: Entity clustering with Louvain algorithm
- **Coreference Resolution**: Entity linking and disambiguation

### Retrieval Strategies
- **Vector Retrieval**: Dense embedding-based semantic search
- **Graph Retrieval**: Entity-centric and relationship-aware retrieval
- **Sparse Retrieval**: BM25 keyword matching
- **Hybrid Fusion**: Intelligent combination of multiple strategies

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of excellent open-source projects: Neo4j, spaCy, sentence-transformers
- Inspired by recent advances in Graph RAG and hybrid retrieval systems

## 📞 Contact

For questions and support, please open an issue on GitHub.
