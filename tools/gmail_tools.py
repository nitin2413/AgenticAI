import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config.settings import settings

SCOPES = [settings.SCOPES]
GMAIL_TOKEN_PATH = settings.GMAIL_TOKEN_PATH
GMAIL_CREDENTIALS_PATH = settings.GMAIL_CREDENTIALS_PATH

def get_gmail_service():
    try:
        creds = None

        if os.path.exists(GMAIL_TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)

            os.makedirs(os.path.dirname(GMAIL_TOKEN_PATH), exist_ok=True)
            with open(GMAIL_TOKEN_PATH, "w") as token_file:
                token_file.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        return f"error in calling gmail {e}"


def fetch_recent_emails(max_results=10):
    try:
        service = get_gmail_service()

        results = service.users().messages().list( #   references — message IDs
            userId="me", maxResults=max_results, labelIds=["INBOX"]
        ).execute()
        messages = results.get("messages", []) # actual fetching of the gmail message

        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()

            headers = msg_detail["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")
            date = next((h["value"] for h in headers if h["name"] == "Date"), "(unknown date)")

            emails.append({
                "subject": subject,
                "sender": sender,
                "date": date,
                "snippet": msg_detail.get("snippet", "")
            })

        return emails
    except Exception as e:
        return f"error in retrieving email from gmail : {e}"
