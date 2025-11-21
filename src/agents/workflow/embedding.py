import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class EmbeddingAgent(BaseAgent):
    """
    Agent responsible for generating embeddings for text chunks.
    """
    def __init__(self, name: str, model_name: str = "all-MiniLM-L6-v2"):
        super().__init__(name=name)
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate embeddings.
        Task format: {'texts': List[str]}
        """
        texts = task.get("texts", [])
        if not texts:
            return {"error": "No texts provided"}

        if not self.model:
            return {"error": "Embedding model not loaded"}

        try:
            embeddings = self.model.encode(texts).tolist()
            return {
                "status": "success",
                "embeddings": embeddings,
                "count": len(embeddings)
            }
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    pass
