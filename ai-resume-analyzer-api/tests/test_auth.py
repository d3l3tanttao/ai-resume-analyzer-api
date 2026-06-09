def test_register_user_returns_created_user(client, unique_email, test_password):
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": test_password,
            "full_name": "Test User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == unique_email
    assert data["full_name"] == "Test User"
    assert data["is_active"] is True
    assert "id" in data
    assert "hashed_password" not in data


def test_register_user_with_duplicate_email_returns_409(
    client,
    unique_email,
    test_password,
):
    payload = {
        "email": unique_email,
        "password": test_password,
        "full_name": "Test User",
    }

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "User with this email already exists."


def test_login_returns_access_token(client, unique_email, test_password):
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": test_password,
            "full_name": "Login User",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": test_password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password_returns_401(client, unique_email, test_password):
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": test_password,
            "full_name": "Login User",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_get_me_returns_current_user(client, unique_email, test_password):
    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": test_password,
            "full_name": "Current User",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": test_password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == unique_email
    assert data["full_name"] == "Current User"
    assert data["is_active"] is True