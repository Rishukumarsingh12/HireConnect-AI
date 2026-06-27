from sqlalchemy.orm import Session
from app.services.gmail_services import GmailService
from app.database.models import (
    Recruiter,
    GeneratedEmail
)

from app.agent.company_research_agent import (
    CompanyResearchAgent
)

from app.agent.project_matching_agent import (
    ProjectMatchingAgent
)

from app.agent.email_generation_agent import (
    EmailGenerationAgent
)


class OutreachPipelineService:

    def __init__(self):

        self.company_agent = CompanyResearchAgent()

        self.matching_agent = ProjectMatchingAgent()

        self.email_agent = EmailGenerationAgent()

        self.gmail_service = GmailService()

    def generate_draft(
        self,
        db: Session,
        recruiter: Recruiter
    ):

        company_result = (
            self.company_agent.research(
                recruiter.company
            )
        )

        if not company_result["success"]:
            return company_result

        matching_result = (
            self.matching_agent.match(
                company_result["data"]
            )
        )

        if not matching_result["success"]:
            return matching_result

        email_result = (
            self.email_agent.generate(
                recruiter_name=recruiter.name,
                recruiter_title=recruiter.title,
                company_context=company_result["data"],
                matching_result=matching_result["data"]
            )
        )

        if not email_result["success"]:
            return email_result

        draft = GeneratedEmail(

            recruiter_id=recruiter.id,

            subject=email_result["data"]["subject"],

            body=email_result["data"]["body"],

            status="draft",

            company_analysis=company_result["data"],

            project_matching={
                "reason":
                matching_result["data"]["reason"]
            }
        )

        db.add(draft)

        db.commit()

        db.refresh(draft)

        return {
            "success": True,
            "draft_id": draft.id
        }
    
    def create_gmail_draft(
    self,
    db: Session,
    generated_email_id: int
):

        email = (
            db.query(GeneratedEmail)
            .filter(
                GeneratedEmail.id == generated_email_id
            )
            .first()
        )

        if not email:

            return {
                "success": False,
                "error": "Generated email not found"
            }

        recruiter = (
            db.query(Recruiter)
            .filter(
                Recruiter.id == email.recruiter_id
            )
            .first()
        )

        if not recruiter:

            return {
                "success": False,
                "error": "Recruiter not found"
            }

        result = self.gmail_service.create_draft(
            recipient_email=recruiter.email,
            subject=email.subject,
            body=email.body
        )

        if not result["success"]:
            return result

        email.status = "gmail_draft"

        db.commit()

        return {
            "success": True,
            "generated_email_id": email.id,
            "gmail_draft_id": result["draft_id"],
            "recipient": recruiter.email
        }

    def generate_first_n_drafts(self,db: Session,limit: int = 10):
    
        recruiters = (
            db.query(Recruiter)
            .limit(limit)
            .all()
        )

        results = []

        for recruiter in recruiters:

            try:

                result = self.generate_draft(
                    db=db,
                    recruiter=recruiter
                )

                results.append({
                    "recruiter":
                    recruiter.email,

                    "result":
                    result
                })

            except Exception as e:

                results.append({
                    "recruiter":
                    recruiter.email,

                    "error":
                    str(e)
                })

        return results
    
    def create_first_n_gmail_drafts(
    self,
    db: Session,
    limit: int = 10
):

        drafts = (
            db.query(GeneratedEmail)
            .filter(
                GeneratedEmail.status == "draft"
            )
            .limit(limit)
            .all()
        )

        results = []

        for draft in drafts:

            try:

                result = self.create_gmail_draft(
                    db=db,
                    generated_email_id=draft.id
                )

                results.append(result)

            except Exception as e:

                results.append({
                    "success": False,
                    "generated_email_id": draft.id,
                    "error": str(e)
                })

        return results

    from sqlalchemy.orm import Session
from app.services.gmail_services import GmailService
from app.database.models import (
    Recruiter,
    GeneratedEmail
)
from app.services.resume_services import ResumeService
from app.agent.company_research_agent import (
    CompanyResearchAgent
)

from app.agent.project_matching_agent import (
    ProjectMatchingAgent
)

from app.agent.email_generation_agent import (
    EmailGenerationAgent
)


class OutreachPipelineService:

    def __init__(self):

        self.company_agent = CompanyResearchAgent()

        self.matching_agent = ProjectMatchingAgent()

        self.email_agent = EmailGenerationAgent()

        self.gmail_service = GmailService()

        self.resume_service = ResumeService()

    def generate_draft(
        self,
        db: Session,
        recruiter: Recruiter,
        Attachments: list = None
    ):

        company_result = (
            self.company_agent.research(
                recruiter.company
            )
        )

        if not company_result["success"]:
            return company_result

        matching_result = (
            self.matching_agent.match(
                company_result["data"]
            )
        )

        if not matching_result["success"]:
            return matching_result

        email_result = (
            self.email_agent.generate(
                recruiter_name=recruiter.name,
                recruiter_title=recruiter.title,
                company_context=company_result["data"],
                matching_result=matching_result["data"]
            )
        )

        if not email_result["success"]:
            return email_result

        draft = GeneratedEmail(

            recruiter_id=recruiter.id,

            subject=email_result["data"]["subject"],

            body=email_result["data"]["body"],

            status="draft",

            company_analysis=company_result["data"],

            project_matching={
                "reason":
                matching_result["data"]["reason"]
            }
        )

        db.add(draft)

        db.commit()

        db.refresh(draft)

        return {
    "success": True,
    "generated_email_id": draft.id,
    "recruiter_id": recruiter.id,
    "recruiter_email": recruiter.email
}
    
    def create_gmail_draft(
    self,
    db: Session,
    generated_email_id: int
):

        email = (
            db.query(GeneratedEmail)
            .filter(
                GeneratedEmail.id == generated_email_id
            )
            .first()
        )

        if not email:

            return {
                "success": False,
                "error": "Generated email not found"
            }

        recruiter = (
            db.query(Recruiter)
            .filter(
                Recruiter.id == email.recruiter_id
            )
            .first()
        )

        if not recruiter:

            return {
                "success": False,
                "error": "Recruiter not found"
            }

        resume_path = self.resume_service.get_best_resume(
            company_context=email.company_analysis,
            matching_result=email.project_matching
        )
        result = self.gmail_service.create_draft(
            recipient_email=recruiter.email,
            subject=email.subject,
            body=email.body,
            attachments=[resume_path]
        )

        if not result["success"]:
            return result

        email.status = "gmail_draft"

        db.commit()

        return {
            "success": True,
            "generated_email_id": email.id,
            "gmail_draft_id": result["draft_id"],
            "recipient": recruiter.email
        }

    def generate_first_n_drafts(self,db: Session,limit: int = 10):
    
        recruiters = (
            db.query(Recruiter)
            .limit(limit)
            .all()
        )

        results = []

        for recruiter in recruiters:

            try:

                result = self.generate_draft(
                    db=db,
                    recruiter=recruiter
                )

                results.append({
                    "recruiter":
                    recruiter.email,

                    "result":
                    result
                })

            except Exception as e:

                results.append({
                    "recruiter":
                    recruiter.email,

                    "error":
                    str(e)
                })

        return results
    
    def create_first_n_gmail_drafts(
    self,
    db: Session,
    limit: int = 10
):

        drafts = (
            db.query(GeneratedEmail)
            .filter(
                GeneratedEmail.status == "draft"
            )
            .limit(limit)
            .all()
        )

        results = []

        for draft in drafts:

            try:

                result = self.create_gmail_draft(
                    db=db,
                    generated_email_id=draft.id
                )

                results.append(result)

            except Exception as e:

                results.append({
                    "success": False,
                    "generated_email_id": draft.id,
                    "error": str(e)
                })

        return results
    def generate_drafts_in_range(
    self,
    db: Session,
    start: int,
    end: int
):

        recruiters = (
            db.query(Recruiter)
            .offset(start - 1)
            .limit(end - start + 1)
            .all()
        )

        results = []

        for recruiter in recruiters:

            try:

                result = self.generate_draft(
                    db=db,
                    recruiter=recruiter
                )

                results.append({
                    "success": result["success"],
                    "generated_email_id": result["generated_email_id"],
                    "recruiter_id": result["recruiter_id"],
                    "recruiter": result["recruiter_email"]
                })

            except Exception as e:

                results.append({
                    "success": False,
                    "recruiter_id": recruiter.id,
                    "recruiter": recruiter.email,
                    "error": str(e)
                })

        return results

    def create_gmail_drafts_in_range(
    self,
    db: Session,
    start: int,
    end: int
):

        drafts = (
            db.query(GeneratedEmail)
            .filter(
                GeneratedEmail.status == "draft"
            )
            .offset(start - 1)
            .limit(end - start + 1)
            .all()
        )

        results = []

        for draft in drafts:

            try:

                result = self.create_gmail_draft(
                    db=db,
                    generated_email_id=draft.id
                )

                results.append(result)

            except Exception as e:

                results.append({
                    "success": False,
                    "generated_email_id": draft.id,
                    "error": str(e)
                })

        return results