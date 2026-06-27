from app.database.connection import SessionLocal
from app.services.outreach_pipeline_services import (
    OutreachPipelineService
)

db = SessionLocal()

pipeline = OutreachPipelineService()
generated = pipeline.generate_drafts_in_range(
    db=db,
    start=58,
    end=108
)
print(generated)
for item in generated:

    if item["success"]:

        result = pipeline.create_gmail_draft(
            db=db,
            generated_email_id=item["generated_email_id"]
        )

        print(result)



db.close()