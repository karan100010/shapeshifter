import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0
    metadata: Dict[str, Any] = {}

class EntityExtractor:
    """
    Entity Extraction Pipeline using spaCy and GLiNER.
    """
    def __init__(self, model_name: str = "en_core_web_sm", use_gliner: bool = False):
        self.model_name = model_name
        self.use_gliner = use_gliner
        self.nlp = None
        self.gliner_model = None
        self._load_models()

    def _load_models(self):
        """Load NLP models."""
        try:
            import spacy
            try:
                self.nlp = spacy.load(self.model_name)
                logger.info(f"Loaded spaCy model: {self.model_name}")
            except OSError:
                logger.warning(f"spaCy model '{self.model_name}' not found. Downloading...")
                from spacy.cli import download
                download(self.model_name)
                self.nlp = spacy.load(self.model_name)
        except ImportError:
            logger.error("spaCy not installed. Please install it with `pip install spacy`.")
        
        if self.use_gliner:
            try:
                from gliner import GLiNER
                # Using a small model for default
                self.gliner_model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
                logger.info("Loaded GLiNER model")
            except ImportError:
                logger.warning("GLiNER not installed. Skipping GLiNER initialization.")
            except Exception as e:
                logger.error(f"Failed to load GLiNER: {e}")

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from text using loaded models.
        """
        entities = []
        
        # spaCy extraction
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append(Entity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=1.0, # spaCy doesn't provide confidence by default
                    metadata={"source": "spacy"}
                ))
        
        # GLiNER extraction (if enabled and available)
        if self.use_gliner and self.gliner_model:
            labels = ["Person", "Organization", "Location", "Date", "Product"]
            gliner_ents = self.gliner_model.predict_entities(text, labels)
            for ent in gliner_ents:
                # Avoid duplicates (simple overlap check could be added)
                entities.append(Entity(
                    text=ent["text"],
                    label=ent["label"],
                    start=ent["start"],
                    end=ent["end"],
                    confidence=ent.get("score", 0.0),
                    metadata={"source": "gliner"}
                ))
                
        return entities

    def batch_extract(self, texts: List[str]) -> List[List[Entity]]:
        """
        Batch process multiple texts.
        """
        return [self.extract_entities(text) for text in texts]

if __name__ == "__main__":
    # Simple test
    logging.basicConfig(level=logging.INFO)
    extractor = EntityExtractor(use_gliner=False) # Disable GLiNER for quick test
    text = "Apple Inc. is planning to open a new store in San Francisco on September 12th."
    entities = extractor.extract_entities(text)
    print(f"Extracted {len(entities)} entities:")
    for ent in entities:
        print(f" - {ent.text} ({ent.label})")
