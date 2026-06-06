from pydantic import BaseModel, EmailStr


class RecruiterCreate(BaseModel):
    name: str
    company: str
    email: EmailStr

class RecruiterData(BaseModel):
    name: str
    email: str
    title: str
    company: str
    
class RecruiterResponse(BaseModel):
    id: int
    name: str
    company: str
    email: str

    class Config:
        from_attributes = True