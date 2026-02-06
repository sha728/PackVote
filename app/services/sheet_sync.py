import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.config import settings
from sqlalchemy.orm import Session
from app.models.group_schema import Participant
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = "PLACEHOLDER_SHEET_ID" # TODO: User needs to provide this or we create one

class SheetSyncService:
    def __init__(self, db: Session):
        self.db = db
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If no valid token, let's assume Service Account logic or manual auth flow (omitted for brevity in MVP)
        # Using Service Account is better for server-side
        if settings.GOOGLE_SERVICE_ACCOUNT_FILE:
             from google.oauth2 import service_account
             self.creds = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    def sync_responses(self, group_id: str):
        if not self.creds:
            print("No Google Credentials found.")
            return

        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        # Range relies on the specific form layout
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Form Responses 1!B2:Z").execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        # Simple Logic: Match by Phone Number (Column C assumed) or ID if passed in URL
        # For this MVP, let's look for a unique identifier column or just update based on phone match
        
        # Structure: [Timestamp, Questions..., Participant_ID (if we injected it)]
        # We need to define the Mapping strictly.
        
        for row in values:
            if len(row) < 5: continue
            
            # Hypothetical Mapping based on User's Table
            # 0: Timestamp
            # 1: Name?
            # 2: Email (Key to match)
            # 3: Activities
            # 4: Budget
            # ...
            
            email_input = row[2] 
            
            participant = self.db.query(Participant).filter(
                Participant.group_id == group_id, 
                Participant.email == email_input
            ).first()

            if participant:
                # Store raw row as preferences for now
                participant.preferences = json.dumps(row)
                participant.has_responded = 1
                self.db.commit()
                print(f"Updated preferences for {participant.name}")
