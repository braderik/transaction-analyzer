#!/usr/bin/env python3
"""
Debug script to examine Tiller sheet structure
"""
import sys
from google_sheets_auth import GoogleSheetsAuth
import config

def debug_tiller_sheet():
    """Debug the actual structure of the Tiller sheet"""
    print("🔍 DEBUGGING TILLER SHEET DATA STRUCTURE")
    print("=" * 50)
    
    # Connect to Google Sheets
    auth = GoogleSheetsAuth()
    service = auth.authenticate()
    
    if not service:
        print("❌ Failed to connect to Google Sheets")
        return
    
    try:
        # Get raw data from Transactions sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range='Transactions!A1:Z20'  # Get first 20 rows with all columns
        ).execute()
        
        values = result.get('values', [])
        print(f"✅ Retrieved {len(values)} rows from Transactions sheet")
        
        if not values:
            print("❌ No data found in sheet")
            return
        
        # Show headers (first row)
        print(f"\n📋 HEADERS (Row 1):")
        headers = values[0] if values else []
        for i, header in enumerate(headers):
            print(f"  Column {chr(65+i)}: '{header}'")
        
        print(f"\n📊 SAMPLE DATA (First 5 rows):")
        for i, row in enumerate(values[:6]):  # Show first 6 rows including header
            print(f"Row {i+1}: {row}")
        
        # Check date formats in the data
        if len(values) > 1:
            print(f"\n📅 DATE ANALYSIS:")
            date_column = None
            amount_column = None
            
            # Try to identify date and amount columns
            for i, header in enumerate(headers):
                if 'date' in header.lower():
                    date_column = i
                    print(f"  Found Date column at position {i}: '{header}'")
                if 'amount' in header.lower() or 'value' in header.lower():
                    amount_column = i
                    print(f"  Found Amount column at position {i}: '{header}'")
            
            if date_column is not None and len(values) > 1:
                print(f"  Sample dates from column {chr(65+date_column)}:")
                for i in range(1, min(6, len(values))):
                    if len(values[i]) > date_column:
                        print(f"    Row {i+1}: '{values[i][date_column]}'")
        
        # Try different sheet tabs that might have transaction data
        print(f"\n🔍 CHECKING OTHER SHEET TABS:")
        sheet_metadata = service.spreadsheets().get(spreadsheetId=config.SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            print(f"  • {sheet_name}")
            
            # Check if this might be a transaction sheet
            if any(word in sheet_name.lower() for word in ['transaction', 'trans', 'expense', 'spending']):
                print(f"    ↳ Might contain transaction data!")
        
    except Exception as error:
        print(f"❌ Error: {error}")

if __name__ == "__main__":
    debug_tiller_sheet()