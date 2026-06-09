from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.router import router as auth_router
from app.config import Settings, get_settings
from app.database import check_database_connection, get_db
from app.resumes.router import router as resumes_router
from app.common.logging import setup_logging

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for resume analysis using FastAPI, PostgreSQL, Docker and AI integration.",
    version="0.4.0",
    debug=True,
)

app.include_router(auth_router)
app.include_router(resumes_router)


@app.get("/health", tags=["System"])
def health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }


@app.get("/db-health", tags=["System"])
def database_health_check() -> dict[str, str]:
    check_database_connection()

    return {
        "status": "ok",
        "database": "connected",
    }


@app.get("/db-tables", tags=["System"])
def database_tables(db: Session = Depends(get_db)) -> dict[str, list[str]]:
    result = db.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
        )
    )

    tables = [row[0] for row in result.fetchall()]

    return {"tables": tables}