import logging
import pickle
import os
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class SparseRetrieverAgent(BaseAgent):
    """
    Agent responsible for sparse retrieval using BM25.
    """
    def __init__(self, name: str, index_path: str = "bm25_index.pkl"):
        super().__init__(name=name)
        self.index_path = index_path
        self.bm25 = None
        self.corpus = [] # List of chunk texts
        self.chunk_ids = [] # List of chunk IDs corresponding to corpus
        self._load_index()

    def _load_index(self):
        """Load BM25 index from disk."""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'rb') as f:
                    data = pickle.load(f)
                    self.bm25 = data['bm25']
                    self.corpus = data['corpus']
                    self.chunk_ids = data['chunk_ids']
                logger.info(f"Loaded BM25 index with {len(self.corpus)} documents.")
            except Exception as e:
                logger.error(f"Failed to load BM25 index: {e}")
        else:
            logger.info("No existing BM25 index found.")

    def save_index(self):
        """Save BM25 index to disk."""
        try:
            with open(self.index_path, 'wb') as f:
                pickle.dump({
                    'bm25': self.bm25,
                    'corpus': self.corpus,
                    'chunk_ids': self.chunk_ids
                }, f)
            logger.info("Saved BM25 index.")
        except Exception as e:
            logger.error(f"Failed to save BM25 index: {e}")

    def index_documents(self, documents: List[Dict[str, str]]):
        """
        Build BM25 index from documents.
        documents: List of {'id': str, 'text': str}
        """
        try:
            from rank_bm25 import BM25Okapi
            
            self.chunk_ids = [doc['id'] for doc in documents]
            self.corpus = [doc['text'] for doc in documents]
            
            # Simple tokenization
            tokenized_corpus = [doc.lower().split() for doc in self.corpus]
            
            self.bm25 = BM25Okapi(tokenized_corpus)
            self.save_index()
            logger.info(f"Indexed {len(documents)} documents.")
            
        except ImportError:
            logger.error("rank-bm25 not installed.")
        except Exception as e:
            logger.error(f"Indexing failed: {e}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute sparse retrieval.
        Task format: {'query': str, 'top_k': int}
        """
        query = task.get("query")
        top_k = task.get("top_k", 5)
        
        if not query:
            return {"error": "No query provided"}
            
        if not self.bm25:
            return {"error": "BM25 index not initialized"}

        try:
            tokenized_query = query.lower().split()
            scores = self.bm25.get_scores(tokenized_query)
            
            # Get top_k indices
            top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
            
            results = []
            for i in top_n:
                if scores[i] > 0: # Only return relevant results
                    results.append({
                        "id": self.chunk_ids[i],
                        "text": self.corpus[i],
                        "score": scores[i]
                    })
                
            return {
                "status": "success",
                "results": results,
                "count": len(results)
            }
            
        except Exception as e:
            logger.error(f"Sparse retrieval failed: {e}")
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    pass
