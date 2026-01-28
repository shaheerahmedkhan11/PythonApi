from app.config import Settings
from jose import jwt
from app.schemas import Token
import pytest


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World!"
    assert res.status_code == 200


def test_create_user(client):
    user_data = {"email": "david@example.com", "password": "securepassword"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    assert res.json().get("email") == user_data["email"]


settings = Settings()


def test_login_user(client, test_user):
    user_data = {"username": test_user["email"], "password": test_user["password"]}
    res = client.post("/login/", data=user_data)
    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
