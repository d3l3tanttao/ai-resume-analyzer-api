def build_resume_analysis_prompt(
    resume_text: str,
    target_role: str | None,
) -> str:
    role = target_role or "Python Backend Developer"

    return f"""
You are an experienced technical recruiter and backend engineering interviewer.

Analyze the resume for the target role: {role}.

Return only valid JSON. Do not use Markdown. Do not wrap the JSON in code fences.
The JSON object must have exactly these fields:
{{
  "score": 0,
  "strengths": "string",
  "weaknesses": "string",
  "recommendations": "string"
}}

Rules:
- score must be an integer from 0 to 100
- strengths must be practical and specific
- weaknesses must be honest but constructive
- recommendations must be actionable
- focus on Python backend development

Evaluation criteria:
- Python backend skills
- FastAPI or Django experience
- PostgreSQL and SQL knowledge
- Docker and deployment readiness
- testing practices
- API design
- clarity and measurable impact
- relevance to the target role

Resume text:
{resume_text}
""".strip()