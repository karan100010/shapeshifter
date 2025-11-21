from src.core.database import db_manager
from src.core.models import WorkflowState
import json

class StateStore:
    def __init__(self):
        self.db = db_manager

    async def save_workflow(self, workflow: WorkflowState):
        # Ensure connection
        if not self.db.postgres_conn:
            self.db.connect_postgres()
        
        conn = self.db.postgres_conn
        cursor = conn.cursor()
        
        # Create table if not exists (simple implementation for now)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                workflow_id VARCHAR(255) PRIMARY KEY,
                data JSONB
            )
        """)
        conn.commit()

        # Upsert workflow
        cursor.execute("""
            INSERT INTO workflows (workflow_id, data)
            VALUES (%s, %s)
            ON CONFLICT (workflow_id) 
            DO UPDATE SET data = EXCLUDED.data
        """, (workflow.workflow_id, workflow.model_dump_json()))
        conn.commit()
        cursor.close()

    async def get_workflow(self, workflow_id: str) -> WorkflowState:
        if not self.db.postgres_conn:
            self.db.connect_postgres()
            
        conn = self.db.postgres_conn
        cursor = conn.cursor()
        
        cursor.execute("SELECT data FROM workflows WHERE workflow_id = %s", (workflow_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return WorkflowState.model_validate_json(result[0])
        return None

state_store = StateStore()
