import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class EvaluatorAgent(BaseAgent):
    """
    Agent responsible for evaluating RAG system performance.
    """
    def __init__(self, name: str):
        super().__init__(name=name)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate generation.
        Task format: {'generated': str, 'reference': str}
        """
        generated = task.get("generated")
        reference = task.get("reference")
        
        if not generated or not reference:
            return {"error": "Generated text and reference required"}

        metrics = {
            "rouge": self._compute_rouge(generated, reference),
            "bert_score": self._compute_bert_score(generated, reference)
        }
        
        return {
            "status": "success",
            "metrics": metrics
        }

    def _compute_rouge(self, generated: str, reference: str) -> Dict[str, float]:
        """Compute ROUGE scores."""
        try:
            from rouge_score import rouge_scorer
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
            scores = scorer.score(reference, generated)
            return {
                "rouge1": scores['rouge1'].fmeasure,
                "rougeL": scores['rougeL'].fmeasure
            }
        except ImportError:
            logger.warning("rouge-score not installed.")
            return {}
        except Exception as e:
            logger.error(f"ROUGE computation failed: {e}")
            return {}

    def _compute_bert_score(self, generated: str, reference: str) -> Dict[str, float]:
        """Compute BERTScore."""
        try:
            from bert_score import score
            P, R, F1 = score([generated], [reference], lang="en", verbose=False)
            return {
                "precision": float(P[0]),
                "recall": float(R[0]),
                "f1": float(F1[0])
            }
        except ImportError:
            logger.warning("bert-score not installed.")
            return {}
        except Exception as e:
            logger.error(f"BERTScore computation failed: {e}")
            return {}

if __name__ == "__main__":
    pass
