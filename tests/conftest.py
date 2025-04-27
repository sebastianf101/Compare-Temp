import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.db.models import Base
from app.db.init_db import init_db

@pytest.fixture(scope="session")
def db_engine():
    """Create a test database engine."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a fresh database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close() 