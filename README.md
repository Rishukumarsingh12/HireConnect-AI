# Recruiter Agent

Recruiter Agent is a FastAPI-based recruiting assistant that helps manage recruiter outreach workflows. It supports recruiter management, PDF-based recruiter extraction, and AI-assisted email generation.

## Features

- Store and manage recruiter contact records
- Extract recruiter information from uploaded PDF files
- Generate outreach email drafts through integrated AI services
- Expose a simple REST API for recruiter and extraction workflows
- Persist data locally using SQLAlchemy

## Project Structure

- app/main.py - FastAPI application entry point
- app/routers/ - API endpoints for recruiters, email generation, and extraction
- app/services/ - business logic for PDF processing and AI-assisted tasks
- app/database/ - database connection and models
- app/data/ - sample data and catalogs
- tests/ - automated tests

## Requirements

- Python 3.10+
- pip

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open the API documentation at:
   ```text
   http://127.0.0.1:8000/docs
   ```

## API Overview

- POST /recruiters/ - Create a recruiter
- GET /recruiters/ - List all recruiters
- GET /recruiters/{recruiter_id} - Get one recruiter
- DELETE /recruiters/{recruiter_id} - Delete a recruiter
- POST /email/generate/{recruiter_id} - Generate an outreach email draft
- POST /extraction/pdf - Upload a PDF to extract recruiter information

## Testing

Run the test suite with:

```bash
pytest -q
```

## Notes

- Uploaded files are stored in the uploads directory.
- Sample data and catalogs are included under app/data for local development.
- Keep any credentials or access tokens in your local secure configuration and never commit them to source control.
