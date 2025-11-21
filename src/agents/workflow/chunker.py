import logging
from typing import List, Dict, Any
from src.agents.base import BaseAgent

# Configure logging
logger = logging.getLogger(__name__)

class ChunkerAgent(BaseAgent):
    """
    Agent responsible for splitting documents into chunks.
    """
    def __init__(self, name: str, model_name: str = "en_core_web_sm"):
        super().__init__(name=name)
        self.model_name = model_name
        self.nlp = None
        self._load_model()

    def _load_model(self):
        """Load spaCy model for sentence segmentation."""
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
            logger.warning("spaCy not installed. Sentence chunking will fall back to simple splitting.")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chunk document.
        Task format: {'text': str, 'strategy': str, 'chunk_size': int, 'overlap': int}
        """
        text = task.get("text")
        strategy = task.get("strategy", "fixed")
        chunk_size = task.get("chunk_size", 512)
        overlap = task.get("overlap", 50)
        
        if not text:
            return {"error": "No text provided"}

        if strategy == "sentence" and self.nlp:
            chunks = self._chunk_by_sentence(text, chunk_size, overlap)
        else:
            chunks = self._chunk_fixed_size(text, chunk_size, overlap)
            
        return {
            "status": "success",
            "chunks": chunks,
            "count": len(chunks)
        }

    def _chunk_fixed_size(self, text: str, size: int, overlap: int) -> List[Dict[str, Any]]:
        """Chunk by fixed character count."""
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + size, text_len)
            chunk_text = text[start:end]
            chunks.append({
                "text": chunk_text,
                "start": start,
                "end": end
            })
            start += (size - overlap)
            
        return chunks

    def _chunk_by_sentence(self, text: str, max_size: int, overlap: int) -> List[Dict[str, Any]]:
        """Chunk by sentences, grouping them up to max_size."""
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        chunks = []
        current_chunk = []
        current_len = 0
        
        # Simple greedy grouping
        # Note: Overlap logic for sentences is trickier, skipping for simplicity in this impl
        # or implementing a sliding window over sentences.
        
        # Sliding window over sentences?
        # Let's do simple grouping for now.
        
        for sent in sentences:
            if current_len + len(sent) > max_size and current_chunk:
                # Finalize current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({"text": chunk_text})
                current_chunk = []
                current_len = 0
                
            current_chunk.append(sent)
            current_len += len(sent)
            
        if current_chunk:
            chunks.append({"text": " ".join(current_chunk)})
            
        return chunks

if __name__ == "__main__":
    pass
