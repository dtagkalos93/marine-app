import pytest
from starlette.testclient import TestClient

from app.db.base_class import Base
from app.db.session import engine, get_db, override_get_db
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True, scope="function")
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
