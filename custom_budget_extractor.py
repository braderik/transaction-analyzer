"""
Custom Budget Extractor - Extract budget data from Erik's specific budget format
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from google_sheets_auth import GoogleSheetsAuth
import config


class CustomBudgetExtractor:
    """Extract budget data from Erik's custom budget sheet format"""
    
    def __init__(self):
        self.auth = GoogleSheetsAuth()
        self.service = None
    
    def connect(self):
        """Connect to Google Sheets API"""
        self.service = self.auth.authenticate()
        return self.service is not None
    
    def get_budget_data(self, sheet_name: str = "Budget Forward check") -> Dict[str, Any]:
        """Extract budget data from custom format"""
        if not self.service:
            self.connect()
        
        try:
            # Get more data to capture full budget structure
            result = self.service.spreadsheets().values().get(
                spreadsheetId=config.BUDGET_SPREADSHEET_ID,
                range=f'{sheet_name}!A1:Z50'  # Get larger range
            ).execute()
            
            values = result.get('values', [])
            print(f"✅ Retrieved {len(values)} rows from {sheet_name}")
            
            if not values:
                return {}
            
            # Extract budget information
            budget_data = self._parse_budget_structure(values)
            return budget_data
            
        except Exception as error:
            print(f"❌ Error retrieving budget data: {error}")
            return {}
    
    def _parse_budget_structure(self, values: List[List]) -> Dict[str, Any]:
        """Parse Erik's specific budget structure"""
        budget_info = {
            'current_month_balance': None,
            'projected_balances': {},
            'budget_categories': {},
            'monthly_income': None,
            'monthly_expenses': None,
            'raw_data_preview': values[:10]  # Keep first 10 rows for reference
        }
        
        try:
            # Find current month balance (around July column)
            current_month_col = None
            header_row = values[1] if len(values) > 1 else []  # Month headers in row 2
            
            for i, month in enumerate(header_row):
                if 'July' in str(month) or 'Jul' in str(month):
                    current_month_col = i
                    break
            
            if current_month_col and len(values) > 3:
                # Get current balance from Ally checking row (row 4)
                balance_row = values[3]  # Row 4 has the Ally checking balances
                if len(balance_row) > current_month_col:
                    current_balance = balance_row[current_month_col]
                    budget_info['current_month_balance'] = self._clean_money_value(current_balance)
            
            # Extract income information - look for income rows
            income_found = False
            expense_categories = {}
            
            for i, row in enumerate(values[4:], start=4):  # Start from row 5
                if not row:
                    continue
                
                category_name = str(row[0]).strip() if row else ""
                
                # Skip empty categories
                if not category_name or category_name in ['', 'Instructions']:
                    continue
                
                # Look for income indicators
                if any(word in category_name.lower() for word in ['income', 'salary', 'paycheck', 'wages']):
                    if current_month_col and len(row) > current_month_col:
                        amount = self._clean_money_value(row[current_month_col])
                        if amount and amount > 0:
                            budget_info['monthly_income'] = amount
                            income_found = True
                
                # Look for expense categories
                elif any(word in category_name.lower() for word in ['rent', 'food', 'gas', 'car', 'insurance', 'utilities', 'groceries']):
                    if current_month_col and len(row) > current_month_col:
                        amount = self._clean_money_value(row[current_month_col])
                        if amount:
                            expense_categories[category_name] = abs(amount)  # Make positive for budget
            
            budget_info['budget_categories'] = expense_categories
            
            # Calculate total monthly expenses
            if expense_categories:
                budget_info['monthly_expenses'] = sum(expense_categories.values())
            
            # If no specific income found, estimate from balance changes
            if not income_found and current_month_col and len(values) > 3:
                balance_row = values[3]
                if len(balance_row) > current_month_col + 1:
                    current_bal = self._clean_money_value(balance_row[current_month_col])
                    next_bal = self._clean_money_value(balance_row[current_month_col + 1])
                    if current_bal and next_bal:
                        net_change = next_bal - current_bal
                        if net_change > 0:
                            budget_info['estimated_net_income'] = net_change
            
            print(f"💰 Extracted Budget Summary:")
            print(f"  Current Balance: ${budget_info.get('current_month_balance', 0):.2f}")
            print(f"  Monthly Income: ${budget_info.get('monthly_income', 0):.2f}")
            print(f"  Monthly Expenses: ${budget_info.get('monthly_expenses', 0):.2f}")
            print(f"  Categories Found: {len(expense_categories)}")
            
        except Exception as e:
            print(f"⚠️ Error parsing budget structure: {e}")
        
        return budget_info
    
    def _clean_money_value(self, value) -> float:
        """Clean and convert money values"""
        if not value:
            return 0.0
        
        try:
            # Remove $ and , then convert to float
            cleaned = str(value).replace('$', '').replace(',', '').strip()
            return float(cleaned) if cleaned else 0.0
        except:
            return 0.0
    
    def get_daily_budget_limits(self) -> Dict[str, float]:
        """Convert monthly budget to daily limits for transaction analysis"""
        budget_data = self.get_budget_data()
        
        if not budget_data or not budget_data.get('budget_categories'):
            print("⚠️ Using default budget limits")
            return config.DAILY_BUDGET_LIMITS
        
        # Convert monthly to daily (30 days)
        daily_limits = {}
        monthly_categories = budget_data['budget_categories']
        
        # Map budget sheet categories to our analysis categories
        category_mapping = {
            'Food & Dining': ['food', 'restaurant', 'groceries', 'dining'],
            'Transportation': ['gas', 'car', 'transport', 'fuel', 'auto'],
            'Housing': ['rent', 'mortgage', 'utilities', 'insurance'],
            'Shopping': ['shopping', 'retail', 'amazon'],
            'Entertainment': ['entertainment', 'streaming', 'movies'],
            'Healthcare': ['medical', 'health', 'doctor', 'pharmacy'],
            'Utilities': ['electric', 'water', 'internet', 'phone']
        }
        
        for our_category, keywords in category_mapping.items():
            monthly_budget = 0
            
            # Find matching categories in budget sheet
            for budget_category, amount in monthly_categories.items():
                if any(keyword in budget_category.lower() for keyword in keywords):
                    monthly_budget += amount
            
            # Convert to daily (30 days) if found, otherwise use default
            if monthly_budget > 0:
                daily_limits[our_category] = monthly_budget / 30
            else:
                daily_limits[our_category] = config.DAILY_BUDGET_LIMITS.get(our_category, 25.0)
        
        print(f"📊 Daily Budget Limits (from your sheet):")
        for category, limit in daily_limits.items():
            print(f"  {category}: ${limit:.2f}/day")
        
        return daily_limits


if __name__ == "__main__":
    # Test the extractor
    extractor = CustomBudgetExtractor()
    
    if extractor.connect():
        print("🔗 Connected to Budget Sheet")
        
        # Test budget extraction
        budget_data = extractor.get_budget_data()
        
        if budget_data:
            print("✅ Budget data extracted successfully!")
            
            # Test daily limits conversion
            daily_limits = extractor.get_daily_budget_limits()
            print(f"\n💡 Daily budget limits ready for transaction analysis")
        else:
            print("❌ No budget data extracted")
    else:
        print("❌ Failed to connect to Budget Sheet")