from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.resumes.schemas import ResumeAnalyzeRequest, ResumeAnalysisResponse
from app.resumes.service import (
    create_resume_analysis,
    get_resume_analysis_by_id,
    list_resume_analyses,
)
from app.users.models import User


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/analyze",
    response_model=ResumeAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def analyze_resume(
    payload: ResumeAnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeAnalysisResponse:
    return create_resume_analysis(
        db=db,
        user_id=current_user.id,
        resume_text=payload.resume_text,
        target_role=payload.target_role,
    )


@router.get(
    "",
    response_model=list[ResumeAnalysisResponse],
)
def get_resume_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ResumeAnalysisResponse]:
    return list_resume_analyses(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{analysis_id}",
    response_model=ResumeAnalysisResponse,
)
def get_resume_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeAnalysisResponse:
    analysis = get_resume_analysis_by_id(
        db=db,
        user_id=current_user.id,
        analysis_id=analysis_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume analysis not found.",
        )

    return analysis