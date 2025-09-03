#!/usr/bin/env python3
"""
Debug script to examine your custom budget sheet structure
"""
import sys
from google_sheets_auth import GoogleSheetsAuth
import config

def debug_budget_sheet():
    """Debug the actual structure of your budget sheet"""
    print("🔍 DEBUGGING CUSTOM BUDGET SHEET")
    print("=" * 50)
    
    # Connect to Google Sheets
    auth = GoogleSheetsAuth()
    service = auth.authenticate()
    
    if not service:
        print("❌ Failed to connect to Google Sheets")
        return
    
    try:
        # Get raw data from Budget sheet with broader range
        result = service.spreadsheets().values().get(
            spreadsheetId=config.BUDGET_SPREADSHEET_ID,
            range='Budget Forward Check!A1:Z10'  # First 10 rows, all columns
        ).execute()
        
        values = result.get('values', [])
        print(f"✅ Retrieved {len(values)} rows from Budget sheet")
        
        if not values:
            print("❌ No data found in budget sheet")
            return
        
        # Show headers and structure
        print(f"\n📋 BUDGET SHEET STRUCTURE:")
        max_cols = max(len(row) for row in values) if values else 0
        print(f"Maximum columns found: {max_cols}")
        
        # Show first few rows with column indices
        print(f"\n📊 RAW BUDGET DATA:")
        for i, row in enumerate(values[:5]):  # First 5 rows
            print(f"Row {i+1} ({len(row)} cols): {row}")
        
        # Try to identify budget-relevant columns
        if values:
            headers = values[0] if values else []
            print(f"\n💰 POTENTIAL BUDGET COLUMNS:")
            for i, header in enumerate(headers):
                if any(word in str(header).lower() for word in ['budget', 'amount', 'limit', 'category', 'expense', 'income']):
                    print(f"  Column {chr(65+i)}: '{header}' (Index {i})")
        
        # Check if we can find specific budget values
        print(f"\n🔍 LOOKING FOR BUDGET VALUES:")
        for i, row in enumerate(values[1:6]):  # Skip header, check next 5 rows
            for j, cell in enumerate(row):
                if isinstance(cell, str) and ('$' in cell or cell.replace('.', '').replace('-', '').isdigit()):
                    print(f"  Row {i+2}, Col {chr(65+j)}: '{cell}' (looks like money)")
        
        # Try different sheet names in case the exact name is different
        print(f"\n📑 CHECKING AVAILABLE SHEETS:")
        sheet_metadata = service.spreadsheets().get(spreadsheetId=config.BUDGET_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            print(f"  • {sheet_name}")
            
            # Check if this might contain budget data
            if any(word in sheet_name.lower() for word in ['budget', 'forward', 'check', 'expense', 'planning']):
                print(f"    ↳ Potential budget sheet!")
        
    except Exception as error:
        print(f"❌ Error: {error}")

if __name__ == "__main__":
    debug_budget_sheet()