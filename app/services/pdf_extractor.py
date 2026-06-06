import pdfplumber

from app.schemas.recruiter_data import RecruiterData


def process_pdf(pdf_path: str):

    recruiters = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            for table in tables:

                # Skip header row
                for row in table[1:]:

                    if not row:
                        continue

                    if len(row) < 5:
                        continue

                    recruiter = RecruiterData(
                        name=row[1].strip(),
                        email=row[2].strip(),
                        title=row[3].strip(),
                        company=row[4].strip()
                    )

                    recruiters.append(recruiter)

    return {
        "total_recruiters": len(recruiters),
        "recruiters": recruiters
    }