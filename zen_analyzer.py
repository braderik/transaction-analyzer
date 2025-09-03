"""
Zen MCP Integration for Multi-Model Transaction Analysis
"""
import subprocess
import json
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
import config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ZenAnalyzer:
    """Use Zen MCP Server to analyze transactions with multiple AI models"""
    
    def __init__(self):
        self.zen_path = "/Users/bradyswanson2/zen-mcp-server"
        self.models = config.ZEN_MODELS
    
    def format_transaction_data_for_analysis(self, df: pd.DataFrame, summary: Dict) -> str:
        """Format transaction data for AI analysis"""
        if df.empty:
            return "No transaction data available for analysis."
        
        # Create a comprehensive data summary
        expenses = df[df['Is_Expense']].copy()
        
        analysis_text = f"""
TRANSACTION ANALYSIS DATA
========================
Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}
Total Transactions: {len(df)}
Total Expenses: {len(expenses)}
Total Amount Spent: ${summary.get('total_spent', 0):.2f}

SPENDING BY CATEGORY:
"""
        
        # Add category breakdown
        if not expenses.empty:
            category_summary = expenses.groupby('Category').agg({
                'Abs_Amount': ['sum', 'count', 'mean']
            }).round(2)
            
            for category in category_summary.index:
                total = category_summary.loc[category, ('Abs_Amount', 'sum')]
                count = category_summary.loc[category, ('Abs_Amount', 'count')]
                avg = category_summary.loc[category, ('Abs_Amount', 'mean')]
                budget_limit = config.DAILY_BUDGET_LIMITS.get(category, 0)
                over_budget = total > budget_limit if budget_limit > 0 else False
                
                analysis_text += f"\n{category}:"
                analysis_text += f"\n  - Total: ${total:.2f}"
                analysis_text += f"\n  - Transactions: {count}"
                analysis_text += f"\n  - Average: ${avg:.2f}"
                analysis_text += f"\n  - Budget Limit: ${budget_limit:.2f}"
                analysis_text += f"\n  - Status: {'⚠️ OVER BUDGET' if over_budget else '✅ Within Budget'}\n"
        
        # Add individual transactions for context
        analysis_text += "\nINDIVIDUAL TRANSACTIONS:\n"
        for _, row in expenses.head(20).iterrows():  # Limit to 20 most recent
            analysis_text += f"- {row['Date'].strftime('%Y-%m-%d')}: {row['Description']} | ${row['Abs_Amount']:.2f} | {row['Category']}\n"
        
        if len(expenses) > 20:
            analysis_text += f"... and {len(expenses) - 20} more transactions\n"
        
        return analysis_text
    
    def analyze_with_gemini(self, transaction_data: str, focus: str = "overspending") -> str:
        """Analyze transactions using Gemini Pro via Zen MCP"""
        prompt = f"""
Use zen to analyze the following transaction data with gemini pro. Focus on {focus} patterns and provide actionable insights.

{transaction_data}

Please analyze:
1. Spending patterns and trends
2. Categories where I'm overspending
3. Unusual or concerning transactions
4. Recommendations for budget optimization
5. Behavioral insights about my spending habits

Provide specific, actionable recommendations.
"""
        
        return self._send_to_claude_with_zen(prompt)
    
    def analyze_with_openai(self, transaction_data: str, gemini_insights: str = "") -> str:
        """Analyze transactions using OpenAI O3 via Zen MCP"""
        prompt = f"""
Use zen to analyze the following transaction data with o3. Provide a logical, systematic analysis focusing on financial optimization.

{transaction_data}

Previous Analysis from Gemini Pro:
{gemini_insights}

Please provide:
1. Logical analysis of spending efficiency 
2. Mathematical breakdown of budget variances
3. Risk assessment of current spending patterns
4. Data-driven recommendations for improvement
5. Priority ranking of areas needing attention

Focus on concrete, measurable improvements.
"""
        
        return self._send_to_claude_with_zen(prompt)
    
    def get_consensus_analysis(self, transaction_data: str) -> str:
        """Get consensus analysis from multiple models"""
        prompt = f"""
Use zen consensus to get perspectives from both gemini pro and o3 on my spending patterns. 
I want to understand where I'm overspending and get actionable advice.

Transaction Data:
{transaction_data}

Please get consensus on:
1. Which spending categories need immediate attention
2. What my biggest overspending risks are
3. Top 3 actionable recommendations for improving my budget
4. Whether my current spending patterns are sustainable

I need a balanced perspective that considers both analytical insights and practical advice.
"""
        
        return self._send_to_claude_with_zen(prompt)
    
    def _send_to_claude_with_zen(self, prompt: str) -> str:
        """Send prompt to Claude with Zen MCP integration"""
        try:
            # This would typically be done through Claude Code CLI
            # For now, we'll create a file that can be used with Claude
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt_file = f"/tmp/zen_analysis_prompt_{timestamp}.txt"
            
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            instructions = f"""
💡 MANUAL STEP REQUIRED:
=======================
1. Open Claude Code CLI in terminal: 'claude'
2. Copy and paste this prompt:

{prompt}

3. The results will be your AI-powered transaction analysis!

Prompt saved to: {prompt_file}
"""
            
            return instructions
            
        except Exception as e:
            return f"Error creating Zen analysis prompt: {str(e)}"
    
    def generate_comprehensive_analysis(self, df: pd.DataFrame, summary: Dict) -> Dict[str, str]:
        """Generate comprehensive analysis using multiple AI models"""
        transaction_data = self.format_transaction_data_for_analysis(df, summary)
        
        analyses = {
            'formatted_data': transaction_data,
            'gemini_analysis_prompt': self.analyze_with_gemini(transaction_data),
            'openai_analysis_prompt': self.analyze_with_openai(transaction_data),
            'consensus_prompt': self.get_consensus_analysis(transaction_data)
        }
        
        return analyses


class BudgetAnalyzer:
    """Analyze spending against budgets without AI"""
    
    def __init__(self):
        self.budget_limits = config.DAILY_BUDGET_LIMITS
        self.overspending_threshold = config.OVERSPENDING_THRESHOLD
        self.warning_threshold = config.WARNING_THRESHOLD
    
    def analyze_overspending(self, df: pd.DataFrame) -> Dict:
        """Analyze overspending patterns"""
        if df.empty:
            return {}
        
        expenses = df[df['Is_Expense']].copy()
        category_spending = expenses.groupby('Category')['Abs_Amount'].sum()
        
        overspending_analysis = {
            'overspending_categories': [],
            'warning_categories': [],
            'within_budget': [],
            'total_over_budget': 0,
            'savings_opportunities': []
        }
        
        for category, spent in category_spending.items():
            budget_limit = self.budget_limits.get(category, 0)
            
            if budget_limit == 0:
                continue
            
            percentage_of_budget = spent / budget_limit
            over_amount = spent - budget_limit
            
            if percentage_of_budget >= self.overspending_threshold:
                overspending_analysis['overspending_categories'].append({
                    'category': category,
                    'spent': spent,
                    'budget': budget_limit,
                    'over_by': over_amount,
                    'percentage': percentage_of_budget * 100
                })
                overspending_analysis['total_over_budget'] += over_amount
                
            elif percentage_of_budget >= self.warning_threshold:
                overspending_analysis['warning_categories'].append({
                    'category': category,
                    'spent': spent,
                    'budget': budget_limit,
                    'percentage': percentage_of_budget * 100
                })
            else:
                savings = budget_limit - spent
                overspending_analysis['within_budget'].append({
                    'category': category,
                    'spent': spent,
                    'budget': budget_limit,
                    'savings': savings,
                    'percentage': percentage_of_budget * 100
                })
        
        return overspending_analysis


if __name__ == "__main__":
    # Test the Zen analyzer with sample data
    sample_data = pd.DataFrame({
        'Date': pd.to_datetime(['2025-01-29', '2025-01-29', '2025-01-29']),
        'Description': ['Starbucks Coffee', 'Uber Ride', 'Amazon Purchase'],
        'Amount': [-5.50, -12.00, -45.99],
        'Category': ['Food & Dining', 'Transportation', 'Shopping'],
        'Is_Expense': [True, True, True],
        'Abs_Amount': [5.50, 12.00, 45.99]
    })
    
    sample_summary = {
        'total_spent': 63.49,
        'total_expenses': 3,
        'average_transaction': 21.16
    }
    
    analyzer = ZenAnalyzer()
    analyses = analyzer.generate_comprehensive_analysis(sample_data, sample_summary)
    
    print("🤖 ZEN MCP ANALYSIS PROMPTS GENERATED")
    print("=====================================")
    print("\n📊 Formatted Data:")
    print(analyses['formatted_data'])
    print("\n🎯 Next Steps:")
    print("Copy the prompts above into Claude Code CLI to get AI-powered insights!")