from sqlalchemy import Column, Integer, String
from app.database.connection import Base

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
    recruiter_id = Column(Integer)
    subject = Column(String(255))
    body = Column(String(255))
    status = Column(String(50), default="draft")

    
