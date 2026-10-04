from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import recruiter
from app.routers import email_sender
from app.routers import extraction
from app.routers import pipeline

from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recruiter.router)
app.include_router(email_sender.router)
app.include_router(extraction.router)
app.include_router(pipeline.router)
