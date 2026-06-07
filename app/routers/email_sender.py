from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Recruiter
from app.services.llm_services import LLMService

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)

llm_service = LLMService()

@router.post("/generate/{recruiter_id}")
def generate_email_for_recruiter(
    recruiter_id: int,
    db: Session = Depends(get_db)
):

    recruiter = (
        db.query(Recruiter)
        .filter(
            Recruiter.id == recruiter_id
        )
        .first()
    )

    if not recruiter:
        raise HTTPException(
            status_code=404,
            detail="Recruiter not found"
        )

    result = llm_service.generate_email(
        recruiter_name=recruiter.name,
        recruiter_title=recruiter.title,
        company=recruiter.company
    )

    return {
        "recruiter": recruiter.name,
        "company": recruiter.company,
        "generated_email": result
    }