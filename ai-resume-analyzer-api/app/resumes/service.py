from sqlalchemy.orm import Session

from app.ai.client import analyze_resume_with_ai
from app.config import get_settings
from app.resumes.models import ResumeAnalysis


def generate_mock_resume_analysis(
    resume_text: str,
    target_role: str | None,
) -> dict[str, str | int]:
    score = 70

    lowered_text = resume_text.lower()

    if "python" in lowered_text:
        score += 10

    if "fastapi" in lowered_text:
        score += 10

    if "postgresql" in lowered_text or "postgres" in lowered_text:
        score += 5

    if "docker" in lowered_text:
        score += 5

    score = min(score, 100)

    role_text = target_role or "target role"

    return {
        "score": score,
        "strengths": (
            f"The resume shows relevant technical experience for {role_text}. "
            "It contains several backend-oriented keywords and demonstrates a practical engineering direction."
        ),
        "weaknesses": (
            "The resume could be improved by adding measurable outcomes, clearer project descriptions "
            "and more evidence of testing, deployment and production-level ownership."
        ),
        "recommendations": (
            "Add 2-3 strong backend projects, include concrete technologies, describe business impact, "
            "mention tests and Docker setup, and make the profile summary more focused."
        ),
        "analysis_source": "mock",
    }


def generate_resume_analysis(
    resume_text: str,
    target_role: str | None,
) -> dict[str, str | int]:
    settings = get_settings()

    has_openai_key = (
        settings.openai_api_key is not None
        and settings.openai_api_key.strip()
        and settings.openai_api_key != "your-api-key-here"
    )

    if not has_openai_key:
        return generate_mock_resume_analysis(
            resume_text=resume_text,
            target_role=target_role,
        )

    try:
        ai_result = analyze_resume_with_ai(
            resume_text=resume_text,
            target_role=target_role,
        )

        return {
            "score": ai_result.score,
            "strengths": ai_result.strengths,
            "weaknesses": ai_result.weaknesses,
            "recommendations": ai_result.recommendations,
            "analysis_source": "ai",
        }
    except Exception:
        return generate_mock_resume_analysis(
            resume_text=resume_text,
            target_role=target_role,
        )


def create_resume_analysis(
    db: Session,
    user_id: int,
    resume_text: str,
    target_role: str | None,
) -> ResumeAnalysis:
    analysis_data = generate_resume_analysis(
        resume_text=resume_text,
        target_role=target_role,
    )

    analysis = ResumeAnalysis(
        user_id=user_id,
        resume_text=resume_text,
        target_role=target_role,
        score=int(analysis_data["score"]),
        strengths=str(analysis_data["strengths"]),
        weaknesses=str(analysis_data["weaknesses"]),
        recommendations=str(analysis_data["recommendations"]),
        analysis_source=str(analysis_data.get("analysis_source", "mock")),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def list_resume_analyses(
    db: Session,
    user_id: int,
) -> list[ResumeAnalysis]:
    return (
        db.query(ResumeAnalysis)
        .filter(ResumeAnalysis.user_id == user_id)
        .order_by(ResumeAnalysis.id.desc())
        .all()
    )


def get_resume_analysis_by_id(
    db: Session,
    user_id: int,
    analysis_id: int,
) -> ResumeAnalysis | None:
    return (
        db.query(ResumeAnalysis)
        .filter(
            ResumeAnalysis.id == analysis_id,
            ResumeAnalysis.user_id == user_id,
        )
        .first()
    )