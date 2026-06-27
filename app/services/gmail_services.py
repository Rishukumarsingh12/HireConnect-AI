import os
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import (
    InstalledAppFlow
)
from googleapiclient.discovery import build


class GmailService:

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.compose"
    ]

    def __init__(self):

        self.service = self._authenticate()

    def _authenticate(self):

        creds = None

        if os.path.exists("token.json"):

            creds = Credentials.from_authorized_user_file(
                "token.json",
                self.SCOPES
            )

        if not creds or not creds.valid:

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):

                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None

            if not creds:

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        "credentials.json",
                        self.SCOPES
                    )
                )

                creds = (
                    flow.run_local_server(
                        port=0
                    )
                )

            with open(
                "token.json",
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )

        return build(
            "gmail",
            "v1",
            credentials=creds
        )

    def create_draft(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachments: list[str] | None = None
    ):

        try:

            message = MIMEMultipart()

            message["to"] = recipient_email
            message["subject"] = subject

            message.attach(
                MIMEText(body, "plain")
            )

            # ----------------------------
            # Attach files
            # ----------------------------

            if attachments:

                for file_path in attachments:

                    if not os.path.exists(file_path):
                        continue

                    with open(file_path, "rb") as f:

                        part = MIMEBase(
                            "application",
                            "octet-stream"
                        )

                        part.set_payload(
                            f.read()
                        )

                    encoders.encode_base64(part)

                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{os.path.basename(file_path)}"'
                    )

                    message.attach(part)

            raw_message = (
                base64.urlsafe_b64encode(
                    message.as_bytes()
                )
                .decode()
            )

            draft = {
                "message": {
                    "raw": raw_message
                }
            }

            draft_response = (
                self.service.users()
                .drafts()
                .create(
                    userId="me",
                    body=draft
                )
                .execute()
            )

            return {
                "success": True,
                "draft_id": draft_response["id"]
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }