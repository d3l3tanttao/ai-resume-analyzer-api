from datetime import datetime

from pydantic import BaseModel, Field


class ResumeAnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=50, max_length=20000)
    target_role: str | None = Field(default=None, max_length=255)


class ResumeAnalysisResponse(BaseModel):
    id: int
    user_id: int
    resume_text: str
    target_role: str | None
    score: int
    strengths: str
    weaknesses: str
    recommendations: str
    analysis_source: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }