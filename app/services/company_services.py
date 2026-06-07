import os

from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


class CompanyService:

    def __init__(self):

        self.api_key = os.getenv(
            "SERP_API_KEY"
        )

    def search_company(
        self,
        company_name: str
    ) -> str:

        params = {
            "engine": "google",
            "q": f"{company_name} company overview technology services",
            "api_key": self.api_key
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        snippets = []

        # Knowledge graph
        if "knowledge_graph" in results:

            kg = results["knowledge_graph"]

            if kg.get("title"):
                snippets.append(
                    f"Company: {kg['title']}"
                )

            if kg.get("description"):
                snippets.append(
                    kg["description"]
                )

        # Organic results
        for result in results.get(
            "organic_results",
            []
        )[:5]:

            title = result.get(
                "title",
                ""
            )

            snippet = result.get(
                "snippet",
                ""
            )

            snippets.append(
                f"{title}\n{snippet}"
            )

        return "\n\n".join(snippets)

    def get_company_website(
        self,
        company_name: str
    ):

        params = {
            "engine": "google",
            "q": f"{company_name} official website",
            "api_key": self.api_key
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        organic = results.get(
            "organic_results",
            []
        )

        if organic:

            return organic[0].get("link")

        return None

    def get_company_careers(
        self,
        company_name: str
    ):

        params = {
            "engine": "google",
            "q": f"{company_name} careers jobs",
            "api_key": self.api_key
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        organic = results.get(
            "organic_results",
            []
        )

        if organic:

            return organic[0].get("link")

        return None

    def get_company_description(
        self,
        company_name: str
    ):

        params = {
            "engine": "google",
            "q": f"{company_name} about company",
            "api_key": self.api_key
        }

        search = GoogleSearch(params)

        results = search.get_dict()

        if (
            "knowledge_graph"
            in results
        ):

            return (
                results["knowledge_graph"]
                .get("description")
            )

        return None

    def get_company_website(self, company_name: str):
        pass

    def get_company_careers(self, company_name: str):
        pass

    def get_company_description(self, company_name: str):
        pass