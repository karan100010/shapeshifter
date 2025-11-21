# Contributing to RAG Enhanced Architecture

Thank you for your interest in contributing to the RAG Enhanced Architecture project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue using the Bug Report template
3. Include detailed steps to reproduce
4. Provide environment information (OS, Python version, etc.)
5. Add relevant logs or screenshots

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue using the Feature Request template
3. Clearly describe the feature and its benefits
4. Explain the use case and motivation

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (see below)
3. **Write tests** for your changes
4. **Update documentation** as needed
5. **Ensure tests pass** before submitting
6. **Submit a pull request** with a clear description

## Development Workflow

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/shapeshifter.git
cd shapeshifter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Branch Naming Convention

- `feature/` - New features (e.g., `feature/graph-retriever`)
- `fix/` - Bug fixes (e.g., `fix/entity-extraction-bug`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/agent-base-class`)
- `test/` - Test additions or fixes (e.g., `test/integration-tests`)

### Commit Message Format

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(graph-rag): add multi-hop reasoning capability

Implement graph path traversal for complex queries requiring
multiple reasoning steps. Uses Neo4j shortestPath algorithm.

Closes #28
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Code Quality Tools

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
pylint src/

# Type checking
mypy src/
```

### Documentation

- Use Google-style docstrings
- Include examples in docstrings for complex functions
- Update README.md for user-facing changes
- Add inline comments for complex logic

**Example Docstring:**
```python
def retrieve(self, query: str, k: int = 10) -> List[Dict]:
    """Retrieve relevant chunks for a query.
    
    Args:
        query: The search query string
        k: Number of results to return (default: 10)
        
    Returns:
        List of dictionaries containing chunk data and scores
        
    Raises:
        ValueError: If k is less than 1
        
    Example:
        >>> retriever = VectorRetriever()
        >>> results = retriever.retrieve("What is RAG?", k=5)
        >>> print(results[0]['text'])
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_graph_rag.py

# Run tests matching pattern
pytest -k "test_entity"
```

### Writing Tests

- Place tests in `tests/` directory
- Mirror the source code structure
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Use fixtures for common setup
- Aim for >80% code coverage

**Example Test:**
```python
def test_entity_extraction_returns_correct_types():
    """Test that entity extraction returns expected entity types."""
    extractor = EntityExtractor()
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    entities = extractor.extract(text)
    
    assert len(entities) == 3
    assert entities[0]['type'] == 'ORG'
    assert entities[1]['type'] == 'PERSON'
    assert entities[2]['type'] == 'GPE'
```

## Pull Request Process

1. **Update your branch** with the latest main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run tests and linters**:
   ```bash
   pytest
   black .
   flake8 .
   ```

3. **Push to your fork**:
   ```bash
   git push origin your-branch
   ```

4. **Create Pull Request** on GitHub with:
   - Clear title and description
   - Reference related issues
   - Screenshots for UI changes
   - Checklist of changes

5. **Address review comments** and update PR

6. **Squash commits** if requested before merge

## Review Process

- All PRs require at least one approval
- CI/CD checks must pass
- Code coverage should not decrease
- Documentation must be updated
- Breaking changes require discussion

## Project Structure

```
shapeshifter/
├── src/
│   ├── agents/          # Agent implementations
│   ├── control_plane/   # Orchestrator
│   ├── graph_rag/       # Graph RAG components
│   ├── retrieval/       # Retrieval strategies
│   ├── storage/         # Database adapters
│   └── api/             # API endpoints
├── tests/               # Test files
├── docs/                # Documentation
├── config/              # Configuration files
└── scripts/             # Utility scripts
```

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check docs/ directory

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing! 🎉
