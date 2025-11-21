import logging
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class Relationship(BaseModel):
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = {}

class RelationshipExtractor:
    """
    Relationship Extraction Pipeline using spaCy dependency parsing.
    """
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        self.nlp = None
        self._load_model()

    def _load_model(self):
        """Load spaCy model."""
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
            logger.error("spaCy not installed.")

    def extract_relationships(self, text: str) -> List[Relationship]:
        """
        Extract SVO (Subject-Verb-Object) relationships from text.
        """
        relationships = []
        if not self.nlp:
            return relationships

        doc = self.nlp(text)
        
        for token in doc:
            # Look for main verbs
            if token.pos_ == "VERB":
                subject = None
                obj = None
                
                # Find subject
                for child in token.children:
                    if child.dep_ in ("nsubj", "nsubjpass"):
                        subject = self._get_compound_noun(child)
                        break
                
                # Find object
                for child in token.children:
                    if child.dep_ in ("dobj", "attr", "prep"):
                        if child.dep_ == "prep":
                            # Handle prepositional objects (e.g., "lives in London")
                            for grand_child in child.children:
                                if grand_child.dep_ == "pobj":
                                    obj = self._get_compound_noun(grand_child)
                                    break
                        else:
                            obj = self._get_compound_noun(child)
                        if obj:
                            break
                
                if subject and obj:
                    relationships.append(Relationship(
                        subject=subject,
                        predicate=token.lemma_,
                        object=obj,
                        confidence=0.8, # Heuristic confidence
                        metadata={"source": "dependency_parsing"}
                    ))
                    
        return relationships

    def _get_compound_noun(self, token) -> str:
        """
        Get the full compound noun phrase rooted at the token.
        """
        # Simple heuristic: gather left children that are compound/det/adj
        # This can be improved significantly
        parts = []
        for child in token.lefts:
            if child.dep_ in ("compound", "amod", "det", "poss"):
                parts.append(child.text)
        parts.append(token.text)
        for child in token.rights:
             if child.dep_ in ("compound", "amod"):
                parts.append(child.text)
        return " ".join(parts)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extractor = RelationshipExtractor()
    text = "Elon Musk founded SpaceX in 2002. He also leads Tesla."
    rels = extractor.extract_relationships(text)
    print(f"Extracted {len(rels)} relationships:")
    for r in rels:
        print(f" - {r.subject} --[{r.predicate}]--> {r.object}")
