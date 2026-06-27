from app.database.connection import SessionLocal

from app.services.outreach_pipeline_services import (
    OutreachPipelineService
)


def main():

    db = SessionLocal()

    service = (
        OutreachPipelineService()
    )

    result = (
        service.generate_first_n_drafts(
            db=db,
            limit=10
        )
    )

    print(result)

    db.close()


if __name__ == "__main__":
    main()