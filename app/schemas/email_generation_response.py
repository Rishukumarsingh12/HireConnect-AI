from pydantic import BaseModel


class EmailGenerationResponse(BaseModel):

    subject: str

    body: str