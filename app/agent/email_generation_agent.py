from app.services.resume_services import ResumeService
from app.services.llm_services import LLMService

from app.schemas.email_generation_response import (
    EmailGenerationResponse
)

import json

class EmailGenerationAgent:

    def __init__(self):

        self.resume_service = ResumeService()
        self.llm_service = LLMService()

        with open(
            "app/prompts/email_generation_prompts.txt",
            "r",
            encoding="utf-8"
        ) as f:

            self.prompt_template = f.read()

    def generate(
        self,
        recruiter_name: str,
        recruiter_title: str,
        company_context: dict,
        matching_result: dict
    ):
        candidate_context = {

            "name":
            self.resume_service.get_candidate_name(),

            "education":
            self.resume_service.get_education(),

            "experience":
            self.resume_service.get_experience(),

            "skills":
            self.resume_service.get_flattened_skills()
        }

        recruiter_context = {

            "name": recruiter_name,

            "title": recruiter_title
        }

        prompt = (
        self.prompt_template

        .replace(
            "{recruiter_info}",
            json.dumps(
                recruiter_context,
                indent=2
            )
        )

        .replace(
            "{company_info}",
            json.dumps(
                company_context,
                indent=2
            )
        )

        .replace(
            "{candidate_info}",
            json.dumps(
                candidate_context,
                indent=2
            )
        )

        .replace(
            "{matched_projects}",
            json.dumps(
                    [
                    project.model_dump()
                    for project in matching_result["matched_projects"]],
                indent=2
            )
        )
        .replace(
            "{reasons}",
            matching_result.get(
                "reason",
                ""
            )
        )
    )
        
        response = self.llm_service.generate_json(
    prompt=prompt,
   system_prompt="""
You are a professional software engineer.

Generate highly personalized recruiter outreach emails.

Return ONLY valid JSON.

IMPORTANT:
- Do not wrap the response in markdown
- Do not use ```json
- Escape all newlines using \\n
- Ensure the output is valid json.loads() compatible JSON
""",
    temperature=0.7
)
        if "error" in response:

            return {
                "success": False,
                "error": response["error"],
                "raw_response": response.get(
                    "raw_response"
                )
            }
        validated = EmailGenerationResponse(
    **response
)
        return {
    "success": True,
    "data": validated.model_dump()
}