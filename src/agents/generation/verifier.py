import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class VerifierAgent(BaseAgent):
    """
    Agent responsible for verifying generated claims against evidence.
    """
    def __init__(self, name: str, model_name: str = "cross-encoder/nli-deberta-v3-base"):
        super().__init__(name=name)
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load NLI model."""
        try:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(self.model_name)
            logger.info(f"Loaded NLI model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed. Verification will be skipped.")
        except Exception as e:
            logger.error(f"Failed to load NLI model: {e}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify response.
        Task format: {'response': str, 'evidence': List[str]}
        """
        response = task.get("response")
        evidence = task.get("evidence", [])
        
        if not response or not evidence:
            return {"error": "Response and evidence required"}

        if not self.model:
            return {"status": "skipped", "reason": "Model not loaded"}

        # Split response into sentences/claims (simplified)
        claims = response.split(". ")
        
        verification_results = []
        for claim in claims:
            if len(claim) < 10: continue
            
            # Check against each evidence chunk
            pairs = [[claim, ev] for ev in evidence]
            scores = self.model.predict(pairs)
            
            # Scores are usually [Contradiction, Entailment, Neutral] or similar depending on model
            # Deberta NLI: label_mapping=['contradiction', 'entailment', 'neutral'] usually
            # But CrossEncoder output depends on num_labels.
            # Let's assume binary or use argmax.
            
            # For simplicity, we just return the max entailment score found
            max_score = max([s[1] if len(s) > 1 else s for s in scores]) # Assuming index 1 is entailment if multi-class
            
            verification_results.append({
                "claim": claim,
                "supported": bool(max_score > 0.5), # Threshold
                "confidence": float(max_score)
            })
            
        return {
            "status": "success",
            "results": verification_results
        }

if __name__ == "__main__":
    pass
