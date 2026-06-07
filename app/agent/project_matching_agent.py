import json
from urllib import response

from app.services.resume_services import ResumeService
from app.services.llm_services import LLMService

from app.schemas.project_matching_response import (
    ProjectMatchingResponse
)


class ProjectMatchingAgent:

    def __init__(self):

        self.resume_service = ResumeService()
        self.llm_service = LLMService()

        with open(
            "app/prompts/project_matching_prompts.txt",
            "r",
            encoding="utf-8"
        ) as f:

            self.prompt_template = f.read()

    def match(
        self,
        company_context: dict
    ):

        projects = (
            self.resume_service
            .get_project_summaries()
        )

        prompt = (
            self.prompt_template
            .replace(
                "{company_info}",
                json.dumps(
                    company_context,
                    indent=2
                )
            )
            .replace(
                "{projects}",
                json.dumps(
                    projects,
                    indent=2
                )
            )
        )

        try:

            response = (
                self.llm_service
                .generate_json(
                    prompt=prompt,
                    temperature=0
                )
            )
            print("\nMATCHING RESPONSE")
            print(response)
            validated = (
                ProjectMatchingResponse(
                    **response
                )
            )
            matched_projects = []

            for project in validated.matched_projects:

                matched_projects.append(project)

            return {
                "success": True,
                "data": {
                        "matched_projects": matched_projects,
                        "reason": validated.reason
                    }
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }