"""
Transaction Data Retrieval from Google Sheets
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from google_sheets_auth import GoogleSheetsAuth
import config


class TransactionRetriever:
    """Retrieve and process transaction data from Google Sheets"""
    
    def __init__(self):
        self.auth = GoogleSheetsAuth()
        self.service = None
    
    def connect(self):
        """Connect to Google Sheets API"""
        self.service = self.auth.authenticate()
        return self.service is not None
    
    def get_raw_data(self, spreadsheet_id: str = None, range_name: str = None) -> List[List]:
        """Get raw data from Google Sheets"""
        if not self.service:
            self.connect()
        
        spreadsheet_id = spreadsheet_id or config.SPREADSHEET_ID
        range_name = range_name or config.RANGE_NAME
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            print(f"✅ Retrieved {len(values)} rows from Google Sheets")
            return values
            
        except Exception as error:
            print(f"❌ Error retrieving data: {error}")
            return []
    
    def process_transactions(self, raw_data: List[List]) -> pd.DataFrame:
        """Process raw data into structured transaction DataFrame"""
        if not raw_data:
            return pd.DataFrame()
        
        # Tiller format: Date, Description, Category, Amount, Account
        headers = raw_data[0] if raw_data else []
        data_rows = raw_data[1:] if len(raw_data) > 1 else []
        
        # Create DataFrame with Tiller column structure
        tiller_columns = ['Date', 'Description', 'Category', 'Amount', 'Account']
        
        # Process rows to handle Tiller format
        processed_rows = []
        for row in data_rows:
            if len(row) >= 4:  # Must have at least Date, Description, Category, Amount
                # Pad row to match expected columns length
                padded_row = row + [''] * (len(tiller_columns) - len(row))
                processed_rows.append(padded_row[:len(tiller_columns)])
        
        df = pd.DataFrame(processed_rows, columns=tiller_columns)
        
        # Clean and process the data
        df = self._clean_dataframe(df)
        
        return df
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize the transaction data"""
        # Remove empty rows
        df = df.dropna(subset=['Date', 'Description', 'Amount'], how='all')
        
        # Clean and convert Date column
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])  # Remove rows with invalid dates
        
        # Clean and convert Amount column (handle Tiller format like "$3,784.44" and "-$428.00")
        df['Amount'] = df['Amount'].astype(str).str.replace('$', '').str.replace(',', '').str.strip()
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Amount'])  # Remove rows with invalid amounts
        
        # Clean Description
        df['Description'] = df['Description'].astype(str).str.strip()
        
        # Categorize transactions if Category is empty
        df['Category'] = df.apply(self._categorize_transaction, axis=1)
        
        # Add calculated fields
        df['Is_Expense'] = df['Amount'] < 0
        df['Abs_Amount'] = df['Amount'].abs()
        df['Day_of_Week'] = df['Date'].dt.day_name()
        
        return df.sort_values('Date', ascending=False)
    
    def _categorize_transaction(self, row) -> str:
        """Automatically categorize transactions based on description"""
        # If category is already provided and not empty, use it
        if pd.notna(row['Category']) and str(row['Category']).strip():
            return str(row['Category']).strip()
        
        description = str(row['Description']).lower()
        
        # Check against category keywords
        for category, keywords in config.EXPENSE_CATEGORIES.items():
            if category == 'Miscellaneous':
                continue  # Skip miscellaneous for now
            
            for keyword in keywords:
                if keyword.lower() in description:
                    return category
        
        return 'Miscellaneous'
    
    def get_previous_day_transactions(self, target_date: datetime = None) -> pd.DataFrame:
        """Get transactions from the previous day"""
        if target_date is None:
            target_date = datetime.now() - timedelta(days=1)
        
        # Get all data
        raw_data = self.get_raw_data()
        df = self.process_transactions(raw_data)
        
        if df.empty:
            print("⚠️ No transaction data found")
            return df
        
        # Filter for the target date
        target_date_str = target_date.strftime('%Y-%m-%d')
        previous_day_data = df[df['Date'].dt.strftime('%Y-%m-%d') == target_date_str]
        
        print(f"📊 Found {len(previous_day_data)} transactions for {target_date_str}")
        return previous_day_data
    
    def get_date_range_transactions(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get transactions within a date range"""
        raw_data = self.get_raw_data()
        df = self.process_transactions(raw_data)
        
        if df.empty:
            return df
        
        # Filter by date range
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_data = df[mask]
        
        print(f"📊 Found {len(filtered_data)} transactions between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}")
        return filtered_data
    
    def get_spending_summary(self, df: pd.DataFrame) -> Dict:
        """Generate spending summary from transaction data"""
        if df.empty:
            return {}
        
        # Only analyze expenses (negative amounts)
        expenses = df[df['Is_Expense']].copy()
        
        summary = {
            'total_transactions': len(df),
            'total_expenses': len(expenses),
            'total_spent': expenses['Abs_Amount'].sum(),
            'average_transaction': expenses['Abs_Amount'].mean(),
            'largest_expense': expenses['Abs_Amount'].max(),
            'category_breakdown': expenses.groupby('Category')['Abs_Amount'].agg(['sum', 'count', 'mean']).to_dict(),
            'daily_total': expenses['Abs_Amount'].sum()
        }
        
        return summary


if __name__ == "__main__":
    # Test the transaction retriever
    retriever = TransactionRetriever()
    
    if retriever.connect():
        print("🔗 Connected to Google Sheets")
        
        # Test getting yesterday's transactions
        yesterday_transactions = retriever.get_previous_day_transactions()
        print(f"\n📈 Yesterday's Transactions Preview:")
        print(yesterday_transactions.head())
        
        if not yesterday_transactions.empty:
            summary = retriever.get_spending_summary(yesterday_transactions)
            print(f"\n💰 Spending Summary:")
            print(f"Total Spent: ${summary.get('total_spent', 0):.2f}")
            print(f"Number of Expenses: {summary.get('total_expenses', 0)}")
            print(f"Average Transaction: ${summary.get('average_transaction', 0):.2f}")
    else:
        print("❌ Failed to connect to Google Sheets")