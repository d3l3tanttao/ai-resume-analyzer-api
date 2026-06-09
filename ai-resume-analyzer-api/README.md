# AI Resume Analyzer API

AI Resume Analyzer API is a backend project built with Python, FastAPI, PostgreSQL, Docker, SQLAlchemy, Alembic, JWT authentication and pytest.

The API allows users to register, log in, submit resume text for analysis and store analysis history. The resume analysis flow supports AI integration with a local mock fallback for development.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- JWT authentication
- bcrypt password hashing
- Pytest
- OpenAI API integration
- Swagger / OpenAPI

## Features

- User registration
- User login
- JWT access tokens
- Protected current-user endpoint
- Password hashing with bcrypt
- PostgreSQL database models
- Alembic database migrations
- Protected resume analysis endpoints
- Resume analysis history
- AI/mock analysis source tracking
- Structured logging
- Automated API tests

## Project Structure

```text
ai-resume-analyzer-api/
├── app/
│   ├── ai/
│   │   ├── client.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   │
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── service.py
│   │
│   ├── common/
│   │   └── logging.py
│   │
│   ├── resumes/
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── users/
│   │   └── models.py
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── alembic/
├── tests/
├── .env.example
├── alembic.ini
├── requirements.txt
└── run_api.py