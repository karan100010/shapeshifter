import logging
from neo4j import Driver

# Configure logging
logger = logging.getLogger(__name__)

class GraphSchema:
    """
    Manages Neo4j graph schema, constraints, and indexes.
    """
    def __init__(self, driver: Driver):
        self.driver = driver

    def apply_schema(self):
        """Apply all schema constraints and indexes."""
        self.create_constraints()
        self.create_indexes()
        self.create_fulltext_indexes()

    def create_constraints(self):
        """Create uniqueness constraints."""
        queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE",
            # For Entity, we might want unique name+type or just unique name per type?
            # Or just unique canonical_id if we have one.
            # Let's assume 'name' should be unique for now (simplification)
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for q in queries:
                try:
                    session.run(q)
                    logger.info(f"Executed constraint: {q}")
                except Exception as e:
                    logger.error(f"Failed to create constraint: {e}")

    def create_indexes(self):
        """Create performance indexes."""
        queries = [
            "CREATE INDEX IF NOT EXISTS FOR (e:Entity) ON (e.type)",
            "CREATE INDEX IF NOT EXISTS FOR (c:Chunk) ON (c.doc_id)"
        ]
        
        with self.driver.session() as session:
            for q in queries:
                try:
                    session.run(q)
                    logger.info(f"Executed index: {q}")
                except Exception as e:
                    logger.error(f"Failed to create index: {e}")

    def create_fulltext_indexes(self):
        """Create full-text search indexes."""
        # Neo4j 5.x syntax
        queries = [
            """
            CREATE FULLTEXT INDEX entitySearch IF NOT EXISTS
            FOR (n:Entity) ON EACH [n.name]
            """,
            """
            CREATE FULLTEXT INDEX chunkSearch IF NOT EXISTS
            FOR (n:Chunk) ON EACH [n.text]
            """
        ]
        
        with self.driver.session() as session:
            for q in queries:
                try:
                    session.run(q)
                    logger.info(f"Executed fulltext index: {q}")
                except Exception as e:
                    logger.error(f"Failed to create fulltext index: {e}")

if __name__ == "__main__":
    pass
