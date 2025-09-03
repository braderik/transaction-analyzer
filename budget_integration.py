"""
Custom Budget Integration - Pull budget data from separate Google Sheet
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from google_sheets_auth import GoogleSheetsAuth
import config


class BudgetIntegrator:
    """Integrate custom budget data from separate Google Sheet"""
    
    def __init__(self):
        self.auth = GoogleSheetsAuth()
        self.service = None
    
    def connect(self):
        """Connect to Google Sheets API"""
        self.service = self.auth.authenticate()
        return self.service is not None
    
    def get_budget_data(self) -> pd.DataFrame:
        """Retrieve budget data from custom Google Sheet"""
        if not self.service:
            self.connect()
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=config.BUDGET_SPREADSHEET_ID,
                range=config.BUDGET_RANGE_NAME
            ).execute()
            
            values = result.get('values', [])
            print(f"✅ Retrieved {len(values)} rows from Budget sheet")
            
            if not values:
                return pd.DataFrame()
            
            # Process budget data
            df = pd.DataFrame(values[1:], columns=values[0])  # First row as headers
            return self._clean_budget_data(df)
            
        except Exception as error:
            print(f"❌ Error retrieving budget data: {error}")
            return pd.DataFrame()
    
    def _clean_budget_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and process budget data"""
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Convert numeric columns
        for col in df.columns:
            if any(word in col.lower() for word in ['amount', 'budget', 'limit', 'target']):
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
        
        return df
    
    def get_category_budgets(self) -> Dict[str, float]:
        """Extract category budget limits from budget sheet"""
        budget_df = self.get_budget_data()
        
        if budget_df.empty:
            print("⚠️ No budget data found, using default limits")
            return config.DAILY_BUDGET_LIMITS
        
        category_budgets = {}
        
        # Try to map budget sheet categories to our categories
        # This will need customization based on your actual budget sheet structure
        print("📊 Budget Sheet Columns:", budget_df.columns.tolist())
        print("📊 First 3 rows of budget data:")
        print(budget_df.head(3).to_string())
        
        # For now, return default budgets but with a note about customization needed
        print("💡 Custom budget integration set up - sheet structure analysis needed for mapping")
        return config.DAILY_BUDGET_LIMITS
    
    def analyze_budget_vs_actual(self, transactions_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare actual spending against custom budget"""
        budget_limits = self.get_category_budgets()
        
        if transactions_df.empty:
            return {"status": "no_data"}
        
        expenses = transactions_df[transactions_df['Is_Expense']].copy()
        category_spending = expenses.groupby('Category')['Abs_Amount'].sum().to_dict()
        
        budget_analysis = {}
        for category, budget_limit in budget_limits.items():
            actual_spent = category_spending.get(category, 0)
            
            budget_analysis[category] = {
                'budget': budget_limit,
                'actual': actual_spent,
                'difference': budget_limit - actual_spent,
                'percentage_used': (actual_spent / budget_limit * 100) if budget_limit > 0 else 0,
                'status': 'over' if actual_spent > budget_limit else 'under'
            }
        
        return budget_analysis


if __name__ == "__main__":
    # Test budget integration
    integrator = BudgetIntegrator()
    
    if integrator.connect():
        print("🔗 Connected to Budget Sheet")
        budget_data = integrator.get_budget_data()
        
        if not budget_data.empty:
            print(f"✅ Retrieved {len(budget_data)} budget entries")
            print("\n📊 Budget Data Preview:")
            print(budget_data.head().to_string())
        else:
            print("❌ No budget data found")
    else:
        print("❌ Failed to connect to Budget Sheet")