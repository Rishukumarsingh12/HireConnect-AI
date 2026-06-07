from app.services.company_services import CompanyService
from app.services.cache_services import CacheService
from app.services.llm_services import LLMService

from app.schemas.company_research_response import (
    CompanyResearchResponse,
)


class CompanyResearchAgent:

    def __init__(self):

        self.company_service = CompanyService()
        self.llm_service = LLMService()
        self.cache_service = CacheService()

        with open(
            "app/prompts/company_information_prompts.txt",
            "r",
            encoding="utf-8"
        ) as f:

            self.prompt_template = f.read()

    def research(self, company_name: str) -> dict:
        """
        Main entry point
        """

        # Check cache FIRST
        cached_data = self.cache_service.get_company(
            company_name
        )

        if cached_data:

            return {
                "success": True,
                "data": cached_data,
                "source": "cache"
            }

        # Cache miss -> call SerpAPI
        company_data = self.company_service.search_company(
            company_name
        )

        if not company_data:

            return {
                "success": False,
                "error": f"No information found for {company_name}"
            }

        return self.extract_company_metadata(
            company_name=company_name,
            company_data=company_data
        )

    def extract_company_metadata(
        self,
        company_name: str,
        company_data: str
    ) -> dict:

        prompt = self.prompt_template.replace(
            "{company_data}",
            company_data
        )

        try:

            company_json = self.llm_service.generate_json(
                prompt=prompt,
                system_prompt="""
You are a company research analyst.

Analyze the company information carefully.

Return ONLY valid JSON matching the required schema.
""",
                temperature=0
            )

            # Groq returned malformed JSON
            if "error" in company_json:

                return {
                    "success": False,
                    "error": company_json["error"],
                    "raw_response": company_json.get(
                        "raw_response"
                    ),
                    "company_name": company_name
                }

            company_json["company_name"] = company_name

            validated_response = CompanyResearchResponse(
                **company_json
            )

            final_data = validated_response.model_dump()

            # Save to cache
            self.cache_service.save_company(
                company_name,
                final_data
            )

            return {
                "success": True,
                "data": final_data,
                "source": "groq"
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e),
                "company_name": company_name
            }