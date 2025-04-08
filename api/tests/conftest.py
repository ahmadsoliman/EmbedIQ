import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


# Create a test database engine and session factory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """
    Create test database tables before each test, and drop them after.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Run test
    yield

    # Drop tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """
    Create a new database session for a test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """
    Create a test client with database dependency override.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # Override the get_db dependency
    app.dependency_overrides[get_db] = _get_test_db

    # Create test client
    with TestClient(app) as client:
        yield client

    # Clear dependency overrides
    app.dependency_overrides.clear()
