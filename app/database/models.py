from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Text,
    JSON,
    DateTime
)

from app.database.connection import Base

from datetime import datetime

class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    company = Column(String(255))
    title = Column(String(255))
    email = Column(String(255), unique=True, nullable=False, index=True)

class GeneratedEmail(Base):
    __tablename__ = "generated_emails"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer,ForeignKey("recruiters.id"))
    subject = Column(Text)
    body = Column(Text)
    status = Column(String(50), default="draft")
    gmail_draft_id = Column(String(255), unique=True, nullable=True)
    company_analysis = Column(JSON)
    project_matching = Column(JSON)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

