"""
Google Sheets API Authentication and Setup
"""
import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config


class GoogleSheetsAuth:
    """Handle Google Sheets API authentication and service creation"""
    
    def __init__(self):
        self.service = None
        self.creds = None
    
    def authenticate(self):
        """Authenticate and create Google Sheets service"""
        creds = None
        
        # Check if token file exists
        if config.TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(config.TOKEN_FILE), config.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found at {config.CREDENTIALS_FILE}. "
                        "Please download it from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(config.CREDENTIALS_FILE), config.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(config.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.creds = creds
        self.service = build('sheets', 'v4', credentials=creds)
        return self.service
    
    def test_connection(self):
        """Test the connection by reading from a sample spreadsheet"""
        if not self.service:
            self.authenticate()
        
        try:
            # Test with a public sample spreadsheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId='1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms',
                range='Class Data!A2:E'
            ).execute()
            
            values = result.get('values', [])
            print(f"✅ Google Sheets connection successful! Retrieved {len(values)} rows from test sheet.")
            return True
            
        except HttpError as error:
            print(f"❌ Google Sheets connection failed: {error}")
            return False
    
    def get_sheet_info(self, spreadsheet_id):
        """Get information about a spreadsheet"""
        if not self.service:
            self.authenticate()
        
        try:
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', '')
            sheet_names = [sheet.get('properties', {}).get('title', 'Untitled') for sheet in sheets]
            
            return {
                'title': sheet_metadata.get('properties', {}).get('title', 'Untitled'),
                'sheet_names': sheet_names,
                'sheet_count': len(sheet_names)
            }
            
        except HttpError as error:
            print(f"❌ Error getting sheet info: {error}")
            return None


def setup_credentials_instructions():
    """Print instructions for setting up Google Sheets API credentials"""
    print("""
📋 GOOGLE SHEETS API SETUP INSTRUCTIONS
=======================================

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
   
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application"
   - Name it "Transaction Analyzer"
   - Download the JSON file
   
5. Rename the downloaded file to 'credentials.json'
6. Place it in: {config.CREDENTIALS_FILE}

🔧 GOOGLE SHEET SETUP
====================
Your Google Sheet should have columns like:
- Date (A): YYYY-MM-DD format
- Description (B): Transaction description
- Amount (C): Transaction amount (negative for expenses)
- Category (D): Optional category
- Account (E): Optional account name
- Notes (F): Optional notes

Update the SPREADSHEET_ID in config.py with your sheet's ID
(found in the URL: docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit)
""")


if __name__ == "__main__":
    # Test the authentication
    try:
        auth = GoogleSheetsAuth()
        auth.authenticate()
        auth.test_connection()
        print("🎉 Setup complete! Ready to analyze transactions.")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        setup_credentials_instructions()