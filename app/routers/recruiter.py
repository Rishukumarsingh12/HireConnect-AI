from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status

from app.database.connection import get_db
from app.database.models import Recruiter
from app.schemas.recruiters import (
    RecruiterCreate,
    RecruiterResponse
)

router = APIRouter(
    prefix="/recruiters",
    tags=["Recruiters"]
)


@router.post("/",response_model=RecruiterResponse)
def create_recruiter(recruiter: RecruiterCreate,db: Session = Depends(get_db)):
    new_recruiter = Recruiter(
        name=recruiter.name,
        company=recruiter.company,
        email=recruiter.email
    )

    existing_recruiter = db.query(Recruiter).filter(Recruiter.email == recruiter.email).first()
    if existing_recruiter:
        raise HTTPException(status_code=400, detail="Recruiter with this email already exists")
    else:
        db.add(new_recruiter)
        db.commit()
        db.refresh(new_recruiter)

        return new_recruiter


@router.get("/",response_model=list[RecruiterResponse])
def get_recruiters(db: Session = Depends(get_db)):
    all_recruiters = db.query(Recruiter).all()
    return all_recruiters

@router.get("/{recruiter_id}", response_model=RecruiterResponse)
def get_recruiter(recruiter_id: int, db: Session = Depends(get_db)):
    recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    return recruiter

@router.delete("/{recruiter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recruiter(recruiter_id: int, db: Session = Depends(get_db)):
    recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    db.delete(recruiter)
    db.commit()
    return {"detail": "Recruiter deleted successfully"}