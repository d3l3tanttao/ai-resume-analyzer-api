from pydantic import BaseModel, Field


class ResumeAIAnalysis(BaseModel):
    score: int = Field(ge=0, le=100)
    strengths: str
    weaknesses: str
    recommendations: str