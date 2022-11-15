from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base, Post
from app.oauth2 import create_access_token


# postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}_test"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    # before yielding the db, delete all tables to ensure a clean slate
    Base.metadata.drop_all(bind=engine)
    # create tables to run tests
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

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "example@gmail.com", "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_for_delete_test(client):
    user_data = {"email": "example_delete@gmail.com", "password": "password"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, test_user_for_delete_test, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "user_id": test_user["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "user_id": test_user["id"],
        },
        {
            "title": "to delete",
            "content": "to delete",
            "user_id": test_user_for_delete_test["id"],
        },
    ]

    def create_post_model(post: dict):
        return Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()

    queried_posts = session.query(Post).all()

    return queried_posts
