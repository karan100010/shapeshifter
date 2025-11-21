from src.config import settings
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
import redis
import psycopg2
from typing import Optional

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.neo4j_driver = None
            cls._instance.qdrant_client = None
            cls._instance.redis_client = None
            cls._instance.postgres_conn = None
        return cls._instance

    def connect_all(self):
        self.connect_neo4j()
        self.connect_qdrant()
        self.connect_redis()
        self.connect_postgres()

    def connect_neo4j(self):
        try:
            self.neo4j_driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def connect_qdrant(self):
        try:
            self.qdrant_client = QdrantClient(url=settings.QDRANT_URL)
        except Exception as e:
            print(f"Failed to connect to Qdrant: {e}")

    def connect_redis(self):
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True
            )
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")

    def connect_postgres(self):
        try:
            self.postgres_conn = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                dbname=settings.POSTGRES_DB
            )
        except Exception as e:
            print(f"Failed to connect to Postgres: {e}")

    def close(self):
        if self.neo4j_driver:
            self.neo4j_driver.close()
        if self.postgres_conn:
            self.postgres_conn.close()
        if self.redis_client:
            self.redis_client.close()

db_manager = DatabaseManager()
