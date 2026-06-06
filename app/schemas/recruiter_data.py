from pydantic import BaseModel

class RecruiterData(BaseModel):
    name: str
    email: str
    title: str
    company: str