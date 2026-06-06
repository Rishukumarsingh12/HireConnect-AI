from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os

from app.database.connection import get_db
from app.database.models import Recruiter
from app.services.pdf_extractor import process_pdf

router = APIRouter(
    prefix="/extraction",
    tags=["Extraction"]
)


@router.post("/pdf")
async def extract_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    result = process_pdf(file_path)

    recruiters = result["recruiters"]

    saved = 0
    duplicates = 0

    for recruiter_data in recruiters:

        existing = (
            db.query(Recruiter)
            .filter(
                Recruiter.email == recruiter_data.email
            )
            .first()
        )

        if existing:
            duplicates += 1
            continue

        recruiter = Recruiter(
            name=recruiter_data.name,
            email=recruiter_data.email,
            title=recruiter_data.title,
            company=recruiter_data.company
        )

        db.add(recruiter)

        saved += 1

    db.commit()

    return {
        "total_recruiters": len(recruiters),
        "saved": saved,
        "duplicates": duplicates
    }