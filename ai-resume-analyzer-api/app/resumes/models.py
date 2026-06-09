from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    resume_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    target_role: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    strengths: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    weaknesses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    recommendations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    analysis_source: Mapped[str] = mapped_column(
        String(50),
        default="mock",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )