import logging
from neo4j import Driver

# Configure logging
logger = logging.getLogger(__name__)

class CommunityDetector:
    """
    Runs community detection algorithms using Neo4j Graph Data Science (GDS).
    """
    def __init__(self, driver: Driver):
        self.driver = driver

    def run_louvain(self, graph_name: str = "entityGraph", write_property: str = "communityId"):
        """
        Run Louvain community detection.
        1. Project the graph (if not exists).
        2. Run Louvain and write results.
        3. Drop the projection.
        """
        self._project_graph(graph_name)
        
        query = f"""
        CALL gds.louvain.write($graph_name, {{
            writeProperty: $write_property
        }})
        YIELD communityCount, modularity, ranIterations
        """
        
        with self.driver.session() as session:
            try:
                result = session.run(query, graph_name=graph_name, write_property=write_property)
                record = result.single()
                if record:
                    logger.info(f"Louvain completed. Communities: {record['communityCount']}, Modularity: {record['modularity']}")
            except Exception as e:
                logger.error(f"Failed to run Louvain: {e}")
            finally:
                self._drop_graph(graph_name)

    def _project_graph(self, graph_name: str):
        """Project the graph into GDS memory."""
        # Check if exists first
        exists_query = "CALL gds.graph.exists($graph_name) YIELD exists RETURN exists"
        
        project_query = """
        CALL gds.graph.project(
            $graph_name,
            'Entity',
            {
                RELATED_TO: {
                    orientation: 'UNDIRECTED'
                }
            }
        )
        """
        
        with self.driver.session() as session:
            try:
                result = session.run(exists_query, graph_name=graph_name)
                if result.single()["exists"]:
                    self._drop_graph(graph_name)
                
                session.run(project_query, graph_name=graph_name)
                logger.info(f"Projected graph: {graph_name}")
            except Exception as e:
                logger.error(f"Failed to project graph: {e}")

    def _drop_graph(self, graph_name: str):
        """Drop the projected graph from GDS memory."""
        query = "CALL gds.graph.drop($graph_name, false)"
        with self.driver.session() as session:
            try:
                session.run(query, graph_name=graph_name)
                logger.info(f"Dropped graph: {graph_name}")
            except Exception as e:
                logger.error(f"Failed to drop graph: {e}")

if __name__ == "__main__":
    pass
