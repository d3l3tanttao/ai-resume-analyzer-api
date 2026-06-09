import json

from openai import OpenAI

from app.ai.prompts import build_resume_analysis_prompt
from app.ai.schemas import ResumeAIAnalysis
from app.config import get_settings


def is_real_openai_key(api_key: str | None) -> bool:
    if api_key is None:
        return False

    if not api_key.strip():
        return False

    if api_key == "your-api-key-here":
        return False

    return True


def analyze_resume_with_ai(
    resume_text: str,
    target_role: str | None,
) -> ResumeAIAnalysis:
    settings = get_settings()

    if not is_real_openai_key(settings.openai_api_key):
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=settings.openai_api_key)

    prompt = build_resume_analysis_prompt(
        resume_text=resume_text,
        target_role=target_role,
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    raw_text = response.output_text
    data = json.loads(raw_text)

    return ResumeAIAnalysis.model_validate(data)