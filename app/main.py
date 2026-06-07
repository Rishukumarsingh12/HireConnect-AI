from fastapi import FastAPI

from app.routers import recruiter
from app.routers import email_sender
from app.routers import extraction

from app.database.connection import engine
from app.database.models import Base

from app.services.pdf_extractor import process_pdf

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(recruiter.router)
app.include_router(email_sender.router)
app.include_router(extraction.router)


