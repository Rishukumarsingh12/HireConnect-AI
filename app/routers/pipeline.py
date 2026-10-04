from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.outreach_pipeline_services import OutreachPipelineService
from app.database.models import Recruiter, GeneratedEmail

router = APIRouter(
    prefix="/pipeline",
    tags=["Pipeline"]
)

pipeline_service = OutreachPipelineService()


@router.post("/generate-drafts")
def generate_drafts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    result = pipeline_service.generate_first_n_drafts(db=db, limit=limit)
    return result


@router.post("/generate-drafts-range")
def generate_drafts_range(
    start: int,
    end: int,
    db: Session = Depends(get_db)
):
    result = pipeline_service.generate_drafts_in_range(db=db, start=start, end=end)
    return result


@router.post("/create-gmail-drafts")
def create_gmail_drafts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    result = pipeline_service.create_first_n_gmail_drafts(db=db, limit=limit)
    return result


@router.post("/create-gmail-drafts-range")
def create_gmail_drafts_range(
    start: int,
    end: int,
    db: Session = Depends(get_db)
):
    result = pipeline_service.create_gmail_drafts_in_range(db=db, start=start, end=end)
    return result


@router.get("/generated-emails")
def get_generated_emails(
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(GeneratedEmail)
    if status:
        query = query.filter(GeneratedEmail.status == status)
    return query.order_by(GeneratedEmail.id.desc()).all()
