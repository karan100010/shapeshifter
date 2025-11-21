import pytest
from unittest.mock import MagicMock, patch
from src.agents.workflow.query_analyzer import QueryAnalyzerAgent
from src.agents.workflow.analyzer import DocumentAnalyzerAgent
from src.agents.workflow.chunker import ChunkerAgent

@pytest.mark.asyncio
async def test_query_analyzer():
    agent = QueryAnalyzerAgent("test_analyzer")
    task = {"query": "Compare Apple and Microsoft"}
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert result["analysis"]["intent"] == "comparison"
    assert result["analysis"]["strategy"] == "hybrid"

@pytest.mark.asyncio
async def test_document_analyzer():
    agent = DocumentAnalyzerAgent("test_doc_analyzer")
    task = {"text": "This is a simple test document."}
    
    # Mock langdetect and textstat if not installed
    with patch("src.agents.workflow.analyzer.DocumentAnalyzerAgent._detect_language", return_value="en"):
        with patch("src.agents.workflow.analyzer.DocumentAnalyzerAgent._compute_stats", return_value={"word_count": 6}):
            result = await agent.execute(task)
            
            assert result["status"] == "success"
            assert result["metadata"]["language"] == "en"
            assert result["metadata"]["stats"]["word_count"] == 6

@pytest.mark.asyncio
async def test_chunker():
    agent = ChunkerAgent("test_chunker")
    text = "A" * 1000
    task = {"text": text, "strategy": "fixed", "chunk_size": 100, "overlap": 0}
    
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert len(result["chunks"]) == 10
    assert len(result["chunks"][0]["text"]) == 100
