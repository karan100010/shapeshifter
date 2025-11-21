import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class QueryAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing user queries to determine intent and retrieval strategy.
    """
    def __init__(self, name: str, model_name: str = "en_core_web_sm"):
        super().__init__(name=name)
        self.model_name = model_name
        self.nlp = None
        self._load_model()

    def _load_model(self):
        """Load spaCy model."""
        try:
            import spacy
            try:
                self.nlp = spacy.load(self.model_name)
            except OSError:
                logger.warning(f"spaCy model '{self.model_name}' not found. Downloading...")
                from spacy.cli import download
                download(self.model_name)
                self.nlp = spacy.load(self.model_name)
        except ImportError:
            logger.warning("spaCy not installed. Query analysis will be limited.")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze query.
        Task format: {'query': str}
        """
        query = task.get("query")
        if not query:
            return {"error": "No query provided"}

        analysis = {
            "original_query": query,
            "entities": self._extract_entities(query),
            "intent": self._classify_intent(query),
            "strategy": self._determine_strategy(query),
            "expanded_queries": self._expand_query(query)
        }
        
        return {
            "status": "success",
            "analysis": analysis
        }

    def _extract_entities(self, query: str) -> List[Dict[str, str]]:
        """Extract entities from query."""
        entities = []
        if self.nlp:
            doc = self.nlp(query)
            for ent in doc.ents:
                entities.append({"text": ent.text, "label": ent.label_})
        return entities

    def _classify_intent(self, query: str) -> str:
        """Classify query intent using heuristics."""
        query_lower = query.lower()
        if any(w in query_lower for w in ["compare", "difference", "versus", "vs"]):
            return "comparison"
        if any(w in query_lower for w in ["count", "total", "average", "sum", "how many"]):
            return "aggregation"
        if any(w in query_lower for w in ["how", "why", "explain", "cause"]):
            return "multi_hop" # Likely requires reasoning
        return "factual"

    def _determine_strategy(self, query: str) -> str:
        """Determine retrieval strategy."""
        intent = self._classify_intent(query)
        if intent in ["multi_hop", "comparison"]:
            return "hybrid" # Use both graph and vector
        if intent == "aggregation":
            return "graph" # Graph is better for structured aggregation
        return "vector" # Default to vector for simple factual queries

    def _expand_query(self, query: str) -> List[str]:
        """Generate expanded queries (synonyms, etc.)."""
        # Placeholder for query expansion logic
        return [query]

if __name__ == "__main__":
    pass
