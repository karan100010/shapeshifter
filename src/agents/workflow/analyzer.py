import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class DocumentAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing documents (language detection, quality stats).
    """
    def __init__(self, name: str):
        super().__init__(name=name)

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document.
        Task format: {'text': str, 'metadata': dict}
        """
        text = task.get("text")
        metadata = task.get("metadata", {})
        
        if not text:
            return {"error": "No text provided"}

        analysis = {
            "language": self._detect_language(text),
            "stats": self._compute_stats(text),
            "quality_score": self._compute_quality_score(text)
        }
        
        # Merge with existing metadata
        new_metadata = {**metadata, **analysis}
        
        return {
            "status": "success",
            "metadata": new_metadata
        }

    def _detect_language(self, text: str) -> str:
        """Detect language using langdetect."""
        try:
            from langdetect import detect
            return detect(text)
        except ImportError:
            logger.warning("langdetect not installed.")
            return "unknown"
        except Exception:
            return "unknown"

    def _compute_stats(self, text: str) -> Dict[str, Any]:
        """Compute readability and other stats."""
        stats = {}
        try:
            import textstat
            stats["flesch_reading_ease"] = textstat.flesch_reading_ease(text)
            stats["word_count"] = textstat.lexicon_count(text, removepunct=True)
            stats["sentence_count"] = textstat.sentence_count(text)
        except ImportError:
            logger.warning("textstat not installed.")
            stats["word_count"] = len(text.split())
        except Exception as e:
            logger.error(f"Stats computation failed: {e}")
            
        return stats

    def _compute_quality_score(self, text: str) -> float:
        """Compute a heuristic quality score (0.0 - 1.0)."""
        # Simple heuristic based on length and structure
        if not text.strip():
            return 0.0
            
        score = 1.0
        
        # Penalize very short texts
        if len(text) < 50:
            score *= 0.5
            
        # Penalize if mostly special chars (simplified check)
        # ...
        
        return score

if __name__ == "__main__":
    pass
