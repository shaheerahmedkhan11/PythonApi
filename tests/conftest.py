import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.database import get_db
from app.models import Base
from app import models
from app.oauth2 import create_access_token

# 1. Setup Test Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    # Drop and recreate tables for a clean slate every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Dependency override happens here
    def override_get_db():
        try:
            yield session
        finally:
            pass # The session fixture handles closing, so we do nothing here
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Clear overrides after the test is done
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data = {"email": "david@example.com", "password": "securepassword"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201  # Good practice to verify creation
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def test_posts(test_user, session):
    post_data = [
        {"title": "Test Post 1", "content": "content 1", "owner_id": test_user["id"]},
        {"title": "Test Post 2", "content": "content 2", "owner_id": test_user["id"]},
    ]
    
    session.add_all([models.Post(**post) for post in post_data])
    session.commit()
    return session.query(models.Post).all()