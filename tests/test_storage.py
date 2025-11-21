import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.storage.db import Base
from src.storage.models import Workflow, Agent, User

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_workflow(db):
    workflow = Workflow(id="wf-1", type="test", status="PENDING", params={})
    db.add(workflow)
    db.commit()
    
    retrieved = db.query(Workflow).filter(Workflow.id == "wf-1").first()
    assert retrieved is not None
    assert retrieved.type == "test"
    assert retrieved.status == "PENDING"

def test_create_agent(db):
    agent = Agent(id="agent-1", capabilities=["test"], status="ONLINE")
    db.add(agent)
    db.commit()
    
    retrieved = db.query(Agent).filter(Agent.id == "agent-1").first()
    assert retrieved is not None
    assert retrieved.status == "ONLINE"

def test_create_user(db):
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.commit()
    
    retrieved = db.query(User).filter(User.username == "testuser").first()
    assert retrieved is not None
    assert retrieved.email == "test@example.com"
