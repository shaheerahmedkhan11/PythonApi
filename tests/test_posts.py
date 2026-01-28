from app import models
from tests.database import session


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200


def test_create_post(authorized_client, session):
    post_data = {"title": "New Post", "content": "New Content"}
    res = authorized_client.post("/posts/", json=post_data)
    assert res.status_code == 201
    assert res.json().get("title") == post_data["title"]
    session.commit()


def test_authorized_user_get_single_post(authorized_client, test_posts):
    post = test_posts[0]
    res = authorized_client.get(f"/posts/{post.id}")
    assert res.status_code == 200
    assert res.json().get("Post").get("id") == post.id


def test_authorized_user_delete_post(authorized_client, test_posts, session):
    post = test_posts[0]
    res = authorized_client.delete(f"/posts/{post.id}")
    assert res.status_code == 204
    deleted_post = session.query(models.Post).filter(models.Post.id == post.id).first()
    assert deleted_post is None


def test_authorized_user_update_post(authorized_client, test_posts):
    post = test_posts[0]
    res = authorized_client.put(
        f"/posts/{post.id}",
        json={"title": "Updated Title", "content": "Updated Content"},
    )
    assert res.status_code == 200
    assert res.json().get("title") == "Updated Title"
