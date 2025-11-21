import logging
from typing import List, Dict, Any
from neo4j import Driver

# Configure logging
logger = logging.getLogger(__name__)

class EntityRetriever:
    """
    Retrieves information centered around specific entities.
    """
    def __init__(self, driver: Driver):
        self.driver = driver

    def search_entity(self, query: str) -> List[Dict[str, Any]]:
        """
        Fuzzy search for entities by name.
        """
        # Using fulltext index created in schema.py
        query_cypher = """
        CALL db.index.fulltext.queryNodes("entitySearch", $query) YIELD node, score
        RETURN node.name as name, node.type as type, score
        LIMIT 10
        """
        
        results = []
        with self.driver.session() as session:
            try:
                result = session.run(query_cypher, query=query)
                for record in result:
                    results.append({
                        "name": record["name"],
                        "type": record["type"],
                        "score": record["score"]
                    })
            except Exception as e:
                logger.error(f"Entity search failed: {e}")
                
        return results

    def get_entity_context(self, entity_name: str) -> Dict[str, Any]:
        """
        Get context for an entity (neighbors, related chunks).
        """
        query = """
        MATCH (e:Entity {name: $name})
        OPTIONAL MATCH (e)-[r]-(related:Entity)
        OPTIONAL MATCH (e)<-[:MENTIONS]-(c:Chunk)
        RETURN e, collect(distinct related) as neighbors, collect(distinct c) as chunks
        """
        
        context = {}
        with self.driver.session() as session:
            result = session.run(query, name=entity_name)
            record = result.single()
            if record:
                context = {
                    "entity": record["e"]["name"],
                    "neighbors": [n["name"] for n in record["neighbors"]],
                    "chunks": [c["text"] for c in record["chunks"]]
                }
                
        return context

if __name__ == "__main__":
    pass
