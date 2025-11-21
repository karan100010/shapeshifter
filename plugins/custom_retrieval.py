"""
Example Custom Retrieval Plugin

This demonstrates how to create a custom retrieval plugin.
"""

from typing import List, Dict, Any
from src.plugins import RetrievalPlugin


class CustomRetrievalPlugin(RetrievalPlugin):
    """Example custom retrieval plugin using keyword matching"""
    
    VERSION = "1.0.0"
    DESCRIPTION = "Custom keyword-based retrieval plugin"
    AUTHOR = "Shapeshifter Team"
    
    def initialize(self) -> bool:
        """Initialize the plugin"""
        self.logger.info("Initializing CustomRetrievalPlugin")
        
        # Load or initialize retrieval index
        self.documents = self.config.get("documents", [])
        
        return True
    
    def retrieve(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve documents using simple keyword matching
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of matching documents
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score documents by keyword overlap
        scored_docs = []
        for doc in self.documents:
            content = doc.get("content", "").lower()
            content_words = set(content.split())
            
            # Calculate overlap score
            overlap = len(query_words & content_words)
            if overlap > 0:
                scored_docs.append({
                    "document": doc,
                    "score": overlap,
                    "matched_words": list(query_words & content_words)
                })
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        self.logger.info("Cleaning up CustomRetrievalPlugin")
        self.documents = []
