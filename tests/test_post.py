import pytest
from app import models
from app.schemas import PostResponse, PostVote


def test_authorized_user_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate_post(post: dict):
        return PostVote(**post)

    post_map = map(validate_post, res.json())
    posts = list(post_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

    for i in range(len(posts)):
        assert posts[i].Post.id == test_posts[i].id
        assert posts[i].Post.title == test_posts[i].title
        assert posts[i].Post.content == test_posts[i].content
        assert posts[i].Post.published == test_posts[i].published
        assert posts[i].Post.user_id == test_posts[i].user_id


def test_authorized_user_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = PostVote(**res.json())

    assert res.status_code == 200

    i = 0

    assert post.Post.id == test_posts[i].id
    assert post.Post.title == test_posts[i].title
    assert post.Post.content == test_posts[i].content
    assert post.Post.published == test_posts[i].published
    assert post.Post.user_id == test_posts[i].user_id


def test_authorized_user_get_posts_by_non_existing_id(authorized_client, test_posts):
    res = authorized_client.get("/posts/888888")

    assert res.status_code == 404


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_posts_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_unauthorized_user_get_posts_by_non_existing_id(client, test_posts):
    res = client.get(f"/posts/888888")

    assert res.status_code == 401


@pytest.mark.parametrize(
    "title, content, published, status_code",
    [
        ("created title 1", "created content 1", True, 201),
        ("created title 2", "created content 2", False, 201),
        (None, "created content 1", True, 422),
        ("created title 2", None, False, 422),
    ],
)
def test_authorized_user_create_post(
    authorized_client, test_user, title, content, published, status_code
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    assert res.status_code == status_code

    if status_code == 201:
        created_post = PostResponse(**res.json())

        assert created_post.title == title
        assert created_post.content == content
        assert created_post.published == published
        assert created_post.user_id == test_user["id"]
        assert created_post.user.email == test_user["email"]


def test_authorized_user_create_post_default_published_true(
    authorized_client, test_user
):
    res = authorized_client.post(
        "/posts/", json={"title": "created title", "content": "created content"}
    )

    created_post = PostResponse(**res.json())

    assert res.status_code == 201

    assert created_post.title == "created title"
    assert created_post.content == "created content"
    assert created_post.published == True

    assert created_post.user_id == test_user["id"]
    assert created_post.user.email == test_user["email"]


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("created title 1", "created content 1", True),
        ("created title 2", "created content 2", False),
    ],
)
def test_unauthorized_user_create_post(client, title, content, published):
    res = client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    assert res.status_code == 401


def test_unauthorized_user_create_post_default_published_true(client):
    res = client.post(
        "/posts/", json={"title": "created title", "content": "created content"}
    )

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_successful_authorized_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_unsuccessful_authorized_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/888888")

    assert res.status_code == 404


def test_delete_post_belonging_to_other_user(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_authorized_user_update_post(authorized_client, test_posts, session):
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "updated title", "content": "updated content"},
    )

    updated_post = PostResponse(**res.json())

    assert res.status_code == 200

    post = session.query(models.Post).filter(models.Post.id == test_posts[0].id).first()

    assert post.title == "updated title"
    assert post.content == "updated content"


def test_authorized_user_update_post_by_non_existing_id(authorized_client, test_posts):
    res = authorized_client.put(
        "/posts/888888",
        json={"title": "updated title", "content": "updated content"},
    )

    assert res.status_code == 404


def test_update_post_belonging_to_other_user(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={"title": "updated title", "content": "updated content"},
    )

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "updated title", "content": "updated content"},
    )

    assert res.status_code == 401
