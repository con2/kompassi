# NOTE: to run, pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

import json
import os.path
from dataclasses import asdict, dataclass
from functools import cache

from django.core.management.base import BaseCommand

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "14J2acRKFBpQ_PoZQAKsuMHv1GFEhuCNxoX2FZSuDVtI"
SAMPLE_RANGE_NAME = "Name split try1!A1:H453"


def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


@cache
def get_signup_data(spreadsheet_id=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME):
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    return result["values"]


@dataclass
class Participant:
    first_name: str
    surname: str
    email: str

    @classmethod
    def from_google_sheets(cls, header_row: list[str], data_row: list[str]):
        player_data = dict(zip(header_row, data_row, strict=True))
        return cls(
            first_name=player_data["First name"],
            surname=player_data["Last name"],
            email=player_data["Email address"],
        )


class Command(BaseCommand):
    args = ""
    help = "Extract solmukohta2020 participants from google sheets"

    def handle(self, *args, **opts):
        signup_data = get_signup_data()
        header_row = signup_data.pop(0)
        participants = [Participant.from_google_sheets(header_row, data_row) for data_row in signup_data]
        print(json.dumps([asdict(ptp) for ptp in participants], indent=2))
