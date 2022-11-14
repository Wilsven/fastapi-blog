import pytest

from app import models


@pytest.fixture
def test_vote(session, test_user, test_posts):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])

    session.add(new_vote)
    session.commit()


def test_authorized_user_vote_up_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "direction": 1}
    )

    assert res.status_code == 201


def test_authorized_user_vote_down_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "direction": 0}
    )

    assert res.status_code == 201


def test_authorized_user_vote_up_on_post_twice(
    authorized_client, test_posts, test_vote
):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "direction": 1}
    )

    assert res.status_code == 409


def test_authorized_user_vote_not_found_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "direction": 0}
    )

    assert res.status_code == 404


@pytest.mark.parametrize("direction", [(0), (1)])
def test_authorized_user_vote_on_non_existent_post(
    authorized_client, test_posts, direction
):
    res = authorized_client.post(
        "/votes/", json={"post_id": 888888, "direction": direction}
    )

    assert res.status_code == 404


@pytest.mark.parametrize("direction", [(0), (1)])
def test_unauthorized_user_vote_on_non_existent_post(client, test_posts, direction):
    res = client.post(
        "/votes/", json={"post_id": test_posts[0].id, "direction": direction}
    )

    assert res.status_code == 401
