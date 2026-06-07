from pydantic import BaseModel


class MatchedProject(BaseModel):
    id: str
    name: str
    category: str
    skills: list[str]
    keywords: list[str]
    priority: int


class ProjectMatchingResponse(BaseModel):
    matched_projects: list[MatchedProject]
    reason: str