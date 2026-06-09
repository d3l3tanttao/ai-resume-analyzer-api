def register_and_login(client, email: str, password: str) -> str:
    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Resume User",
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return login_response.json()["access_token"]


def test_analyze_resume_requires_authentication(client):
    response = client.post(
        "/resumes/analyze",
        json={
            "resume_text": (
                "Python backend developer with experience building REST APIs using "
                "FastAPI, PostgreSQL, Docker, SQLAlchemy, Alembic and Pytest."
            ),
            "target_role": "Python Backend Developer",
        },
    )

    assert response.status_code == 401


def test_analyze_resume_returns_analysis(
    client,
    unique_email,
    test_password,
):
    token = register_and_login(
        client=client,
        email=unique_email,
        password=test_password,
    )

    response = client.post(
        "/resumes/analyze",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "resume_text": (
                "Python backend developer with experience building REST APIs using "
                "FastAPI, PostgreSQL, Docker, SQLAlchemy, Alembic and Pytest. "
                "Worked on authentication, database models, migrations, API documentation "
                "and backend services."
            ),
            "target_role": "Python Backend Developer",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["target_role"] == "Python Backend Developer"
    assert data["score"] >= 0
    assert data["score"] <= 100
    assert data["analysis_source"] in ["mock", "ai"]
    assert "strengths" in data
    assert "weaknesses" in data
    assert "recommendations" in data


def test_list_resume_analyses_returns_user_items(
    client,
    unique_email,
    test_password,
):
    token = register_and_login(
        client=client,
        email=unique_email,
        password=test_password,
    )

    client.post(
        "/resumes/analyze",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "resume_text": (
                "Python backend developer with FastAPI, PostgreSQL, Docker, Pytest "
                "and REST API experience. Built backend services and database models."
            ),
            "target_role": "Python Backend Developer",
        },
    )

    response = client.get(
        "/resumes",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["target_role"] == "Python Backend Developer"