from jose import jwt
import pytest
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.schemas import Token, UserOut


def test_successful_create_user(client):
    res = client.post(
        "/users/", json={"email": "example@gmail.com", "password": "password"}
    )
    new_user = UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "example@gmail.com"


def test_unsuccessful_create_existing_user(client, test_user):
    with pytest.raises(IntegrityError):
        client.post(
            "/users/", json={"email": "example@gmail.com", "password": "password"}
        )


def test_successful_login(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    token = Token(**res.json())
    payload = jwt.decode(
        token.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user["id"]
    assert token.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password",
    [
        ("wrongemail@gmail.com", "password"),
        ("example@gmail.com", "wrongpassword"),
        ("wrongemail@gmail.com", "wrongpassword"),
    ],
)
def test_unsuccessful_login(client, test_user, email, password):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == 403
    assert res.json().get("detail") == "Invalid credentials"


@pytest.mark.parametrize(
    "email, password",
    [
        (None, "password"),
        ("example@gmail.com", None),
    ],
)
def test_unsuccessful_login_missing_fields(client, test_user, email, password):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == 422
    assert res.json().get("detail")[0].get("msg") == "field required"
