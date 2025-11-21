import logging
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver

# Configure logging
logger = logging.getLogger(__name__)

class GraphConstructor:
    """
    Constructs the knowledge graph in Neo4j from extracted entities and relationships.
    """
    def __init__(self, driver: Driver):
        self.driver = driver

    def close(self):
        if self.driver:
            self.driver.close()

    def create_document_node(self, doc_id: str, metadata: Dict[str, Any]):
        """Create a Document node."""
        query = """
        MERGE (d:Document {id: $doc_id})
        SET d += $metadata
        """
        with self.driver.session() as session:
            session.run(query, doc_id=doc_id, metadata=metadata)
            logger.info(f"Created Document node: {doc_id}")

    def create_chunk_node(self, chunk_id: str, doc_id: str, text: str, metadata: Dict[str, Any]):
        """Create a Chunk node and link it to its Document."""
        query = """
        MERGE (c:Chunk {id: $chunk_id})
        SET c.text = $text, c += $metadata
        WITH c
        MATCH (d:Document {id: $doc_id})
        MERGE (d)-[:HAS_CHUNK]->(c)
        """
        with self.driver.session() as session:
            session.run(query, chunk_id=chunk_id, doc_id=doc_id, text=text, metadata=metadata)
            logger.info(f"Created Chunk node: {chunk_id} linked to {doc_id}")

    def add_entities(self, chunk_id: str, entities: List[Dict[str, Any]]):
        """
        Add Entity nodes and link them to the Chunk.
        Expected entity format: {'text': str, 'label': str, ...}
        """
        query = """
        MATCH (c:Chunk {id: $chunk_id})
        UNWIND $entities as ent
        MERGE (e:Entity {name: ent.text, type: ent.label})
        MERGE (c)-[:MENTIONS]->(e)
        """
        # Clean entities for Cypher (remove complex objects if any)
        clean_entities = [
            {k: v for k, v in e.items() if isinstance(v, (str, int, float, bool))}
            for e in entities
        ]
        
        with self.driver.session() as session:
            session.run(query, chunk_id=chunk_id, entities=clean_entities)
            logger.info(f"Added {len(entities)} entities to chunk {chunk_id}")

    def add_relationships(self, relationships: List[Dict[str, Any]]):
        """
        Add relationships between entities.
        Expected relationship format: {'subject': str, 'predicate': str, 'object': str}
        """
        query = """
        UNWIND $rels as rel
        MATCH (s:Entity {name: rel.subject})
        MATCH (o:Entity {name: rel.object})
        CALL apoc.create.relationship(s, rel.predicate, {}, o) YIELD rel as r
        RETURN count(r)
        """
        # Note: This requires APOC or dynamic Cypher. 
        # Without APOC, we can't dynamically set relationship types easily in a single query without complex CASE or string formatting.
        # For simplicity/standard Cypher, we might need to iterate or use a fixed set of types.
        # Or we can use string formatting if we trust the predicate (sanitized).
        
        # Let's use a safer approach: iterate in python for dynamic types if APOC isn't guaranteed.
        # But for batching, APOC is best. Assuming APOC might not be there, let's do a simple loop for now or use a generic RELATED_TO with a type property.
        
        # Alternative: MERGE (s)-[:RELATED_TO {type: rel.predicate}]->(o)
        # This is safer and easier.
        
        query_generic = """
        UNWIND $rels as rel
        MERGE (s:Entity {name: rel.subject})
        MERGE (o:Entity {name: rel.object})
        MERGE (s)-[r:RELATED_TO {type: rel.predicate}]->(o)
        """
        
        with self.driver.session() as session:
            session.run(query_generic, rels=relationships)
            logger.info(f"Added {len(relationships)} relationships")

    def link_sequential_chunks(self, prev_chunk_id: str, next_chunk_id: str):
        """Link sequential chunks with NEXT relationship."""
        query = """
        MATCH (p:Chunk {id: $prev_id})
        MATCH (n:Chunk {id: $next_id})
        MERGE (p)-[:NEXT]->(n)
        """
        with self.driver.session() as session:
            session.run(query, prev_id=prev_chunk_id, next_id=next_chunk_id)

if __name__ == "__main__":
    # Test stub
    pass
