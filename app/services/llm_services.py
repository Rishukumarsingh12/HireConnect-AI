import os, re
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.default_model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def generate_response(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0,
        max_tokens: int = 8192,
        model: str | None = None
    ) -> str:

        response = self.client.chat.completions.create(
            model=model or self.default_model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0,
        max_tokens: int = 8192,
        model: str | None = None
    ) -> dict:

        response_text = self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model
        )

        try:

            # Remove markdown code fences
            cleaned_response = re.sub(
                r"```json\s*|```",
                "",
                response_text,
                flags=re.IGNORECASE
            ).strip()

            # Try direct JSON parsing
            return json.loads(cleaned_response)

        except Exception:

            try:
                # Extract JSON object from response if extra text exists
                match = re.search(
                    r"\{.*\}",
                    cleaned_response,
                    re.DOTALL
                )

                if match:
                    return json.loads(match.group())

            except Exception:
                pass

            return {
                "error": "Failed to parse JSON response",
                "raw_response": response_text
            }
            
    def generate_email(
        self,
        recruiter_name: str,
        recruiter_title: str,
        company: str
):

        llm = LLMService()

        prompt = f"""
        Recruiter Name:
        {recruiter_name}

        Recruiter Title:
        {recruiter_title}

        Company:
        {company}

        Generate a recruiter outreach email.

        Return JSON:
        {{
            "subject": "",
            "body": ""
        }}
        """

        return llm.generate_json(
                prompt=prompt,
                system_prompt="""
        You are a professional job applicant.

        Return valid JSON only.
        """,
                temperature=0.7
            )