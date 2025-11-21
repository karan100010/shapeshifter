import logging
from typing import List, Dict, Any
from collections import defaultdict
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class HybridFusionAgent(BaseAgent):
    """
    Agent responsible for fusing results from multiple retrieval methods using RRF.
    """
    def __init__(self, name: str, rrf_k: int = 60):
        super().__init__(name=name)
        self.rrf_k = rrf_k

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute hybrid fusion.
        Task format: {'results': Dict[str, List[Dict]], 'top_k': int}
        results: {'vector': [{'id': '1', ...}, ...], 'sparse': [...]}
        """
        results_map = task.get("results", {})
        top_k = task.get("top_k", 10)
        
        if not results_map:
            return {"error": "No results provided for fusion"}

        try:
            fused_results = self.reciprocal_rank_fusion(results_map)
            return {
                "status": "success",
                "results": fused_results[:top_k],
                "count": len(fused_results[:top_k])
            }
        except Exception as e:
            logger.error(f"Hybrid fusion failed: {e}")
            return {"status": "error", "message": str(e)}

    def reciprocal_rank_fusion(self, results_map: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Perform Reciprocal Rank Fusion.
        """
        scores = defaultdict(float)
        metadata_map = {}
        
        for method, items in results_map.items():
            for rank, item in enumerate(items):
                doc_id = item['id']
                scores[doc_id] += 1.0 / (self.rrf_k + rank + 1)
                
                # Keep metadata from the first occurrence (or merge?)
                if doc_id not in metadata_map:
                    metadata_map[doc_id] = item
                    # Ensure text is preserved
                    if 'text' in item:
                        metadata_map[doc_id]['text'] = item['text']
        
        # Sort by score descending
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        
        fused_results = []
        for doc_id in sorted_ids:
            result = metadata_map[doc_id].copy()
            result['score'] = scores[doc_id]
            result['fusion_rank'] = len(fused_results) + 1
            fused_results.append(result)
            
        return fused_results

if __name__ == "__main__":
    pass
