from sqlalchemy.ext.declarative import declarative_base
from app.oauth2 import create_access_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db
from app.config import settings
from fastapi import testclient
from app.models import Base
from app.main import app
from app import models
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield testclient.TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "david@example.com", "password": "securepassword"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(test_user, session):
    post_data = [
        {
            "title": "Test Post",
            "content": "This is a test post content",
            "user_id": test_user["id"],
        },
        {
            "title": "Test Post 2",
            "content": "This is a test post content 2",
            "user_id": test_user["id"],
        },
        {
            "title": "Test Post 3",
            "content": "This is a test post content 3",
            "user_id": test_user["id"],
        },
    ]
    
    session.add_all([models.Post(**post) for post in post_data])

    session.commit()
    
    posts = session.query(models.Post).all()
    
    return posts