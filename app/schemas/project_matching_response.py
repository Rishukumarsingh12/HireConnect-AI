from pydantic import BaseModel

class ProjectMatchingResponse(BaseModel):
    matched_projects: list[str]
    reason: str

