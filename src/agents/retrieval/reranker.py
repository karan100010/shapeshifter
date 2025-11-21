import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class RerankerAgent(BaseAgent):
    """
    Agent responsible for reranking retrieved documents using a Cross-Encoder.
    """
    def __init__(self, name: str, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        super().__init__(name=name)
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load Cross-Encoder model."""
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(self.model_name)
            logger.info(f"Loaded Cross-Encoder model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed. Reranking will be skipped.")
        except Exception as e:
            logger.error(f"Failed to load Cross-Encoder model: {e}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute reranking.
        Task format: {'query': str, 'documents': List[Dict], 'top_k': int}
        documents: [{'id': '1', 'text': '...'}, ...]
        """
        query = task.get("query")
        documents = task.get("documents", [])
        top_k = task.get("top_k", len(documents))
        
        if not query or not documents:
            return {"error": "Query and documents required for reranking"}
            
        if not self.model:
            logger.warning("Reranker model not loaded, returning original order.")
            return {"status": "success", "results": documents[:top_k]}

        try:
            # Prepare pairs for cross-encoder
            pairs = [[query, doc['text']] for doc in documents if 'text' in doc]
            
            if not pairs:
                return {"status": "success", "results": documents[:top_k]}
                
            scores = self.model.predict(pairs)
            
            # Attach scores and sort
            for i, doc in enumerate(documents):
                if i < len(scores):
                    doc['rerank_score'] = float(scores[i])
                else:
                    doc['rerank_score'] = -1.0
            
            # Sort by rerank_score descending
            reranked_docs = sorted(documents, key=lambda x: x.get('rerank_score', -1.0), reverse=True)
            
            return {
                "status": "success",
                "results": reranked_docs[:top_k],
                "count": len(reranked_docs[:top_k])
            }
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    pass
