"""
Configuration settings for the Transaction Analyzer
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIALS_FILE = PROJECT_ROOT / 'credentials.json'
TOKEN_FILE = PROJECT_ROOT / 'token.json'

# User's Google Sheet settings
SPREADSHEET_ID = '1L2NAfkWlLMcGKXqABI2NADn4hXhIwLEUEqLZ_DtlpNU'  # Your transaction sheet
RANGE_NAME = 'Transactions!B:F'  # Skip empty column A, use Tiller columns B-F

# Custom Budget Sheet
BUDGET_SPREADSHEET_ID = '1HssSc2Rm1XnZ_VeCUVbiH4XlCvqM1TrClad3DbzXwzk'  # Your budget sheet
BUDGET_RANGE_NAME = 'Budget Forward Check!A:Z'  # Budget data range

# Transaction categories for analysis
EXPENSE_CATEGORIES = {
    'Food & Dining': ['restaurant', 'food', 'dining', 'uber eats', 'doordash', 'grubhub', 'starbucks', 'coffee'],
    'Transportation': ['uber', 'lyft', 'gas', 'parking', 'metro', 'bus', 'taxi', 'car'],
    'Shopping': ['amazon', 'target', 'walmart', 'shopping', 'retail', 'store'],
    'Entertainment': ['netflix', 'spotify', 'movie', 'theater', 'gaming', 'entertainment'],
    'Utilities': ['electric', 'water', 'internet', 'phone', 'cable', 'utility'],
    'Healthcare': ['doctor', 'pharmacy', 'medical', 'health', 'hospital', 'dental'],
    'Subscriptions': ['subscription', 'monthly', 'annual', 'premium', 'plus'],
    'Miscellaneous': []  # Catch-all for uncategorized transactions
}

# Budget limits (daily) - user should customize these
DAILY_BUDGET_LIMITS = {
    'Food & Dining': 50.0,
    'Transportation': 30.0,
    'Shopping': 40.0,
    'Entertainment': 25.0,
    'Utilities': 15.0,
    'Healthcare': 20.0,
    'Subscriptions': 10.0,
    'Miscellaneous': 35.0
}

# Analysis settings
OVERSPENDING_THRESHOLD = 1.2  # 20% over budget considered overspending
WARNING_THRESHOLD = 0.8  # 80% of budget triggers warning

# Zen MCP settings
ZEN_MODELS = {
    'primary_analyst': 'gemini-pro',  # Deep analysis
    'secondary_analyst': 'o3',        # Logic and patterns
    'quick_review': 'flash'           # Quick insights
}