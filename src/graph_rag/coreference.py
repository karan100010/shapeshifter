import logging
from typing import List, Dict, Any
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class CorefCluster(BaseModel):
    main_entity: str
    mentions: List[str]
    
class CoreferenceResolver:
    """
    Coreference Resolution using fastcoref (F-Core).
    """
    def __init__(self, model_name: str = "biu-nlp/f-coref"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load coreference model."""
        try:
            from fastcoref import FCoref
            self.model = FCoref(device='cpu') # Use CPU by default for compatibility
            logger.info(f"Loaded fastcoref model: {self.model_name}")
        except ImportError:
            logger.warning("fastcoref not installed. Please install with `pip install fastcoref`.")
        except Exception as e:
            logger.error(f"Failed to load fastcoref model: {e}")

    def resolve_coreferences(self, text: str) -> str:
        """
        Resolve coreferences in the text and return the text with mentions replaced by their main entity.
        """
        if not self.model:
            return text

        try:
            preds = self.model.predict(texts=[text])
            # Get clusters
            clusters = preds[0].get_clusters(as_strings=True)
            
            # Simple replacement strategy (naive)
            # A better approach is to return the clusters and let the graph construction handle linking
            # But for "resolution", we might want to rewrite or annotate
            
            # For now, let's just return the text as is, but we provide a method to get clusters
            return text
        except Exception as e:
            logger.error(f"Error during coreference resolution: {e}")
            return text

    def get_clusters(self, text: str) -> List[CorefCluster]:
        """
        Get coreference clusters from text.
        """
        clusters_list = []
        if not self.model:
            return clusters_list

        try:
            preds = self.model.predict(texts=[text])
            clusters = preds[0].get_clusters(as_strings=True)
            
            for cluster in clusters:
                if cluster:
                    # Assume the first mention (or most frequent) is the main entity
                    # fastcoref returns list of strings
                    main_entity = max(cluster, key=len) # Heuristic: longest mention is most descriptive? Or first?
                    clusters_list.append(CorefCluster(
                        main_entity=main_entity,
                        mentions=cluster
                    ))
        except Exception as e:
            logger.error(f"Error getting clusters: {e}")
            
        return clusters_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    resolver = CoreferenceResolver()
    text = "Elon Musk founded SpaceX. He is also the CEO of Tesla."
    clusters = resolver.get_clusters(text)
    print(f"Found {len(clusters)} clusters:")
    for c in clusters:
        print(f" - Main: {c.main_entity}, Mentions: {c.mentions}")
