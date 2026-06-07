from pydantic import BaseModel


class CompanyResearchResponse(BaseModel):

    company_name: str

    industry: str

    domain: str

    tech_stack: list[str]

    hiring_focus: list[str]

    keywords: list[str]

    summary: str