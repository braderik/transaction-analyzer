"""
Enhanced AI Analysis - More detailed analysis using multiple AI models
"""
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json


class EnhancedAIAnalyzer:
    """Generate comprehensive AI analysis prompts for detailed financial insights"""
    
    def __init__(self):
        self.analysis_templates = {
            'comprehensive_spending': self._get_comprehensive_template(),
            'budget_deep_dive': self._get_budget_template(),
            'behavioral_patterns': self._get_behavioral_template(),
            'predictive_insights': self._get_predictive_template(),
            'optimization_strategies': self._get_optimization_template()
        }
    
    def generate_enhanced_analysis_prompts(self, 
                                         transactions_df: pd.DataFrame,
                                         budget_analysis: Dict,
                                         summary_stats: Dict) -> Dict[str, str]:
        """Generate multiple detailed AI analysis prompts"""
        
        # Prepare data context
        context = self._prepare_analysis_context(transactions_df, budget_analysis, summary_stats)
        
        enhanced_prompts = {}
        
        for analysis_type, template in self.analysis_templates.items():
            enhanced_prompts[analysis_type] = template.format(**context)
        
        return enhanced_prompts
    
    def _prepare_analysis_context(self, df: pd.DataFrame, budget: Dict, stats: Dict) -> Dict:
        """Prepare comprehensive context for AI analysis"""
        
        if df.empty:
            return self._get_empty_context()
        
        expenses = df[df['Is_Expense']].copy()
        
        # Category breakdown with details
        category_details = []
        for category in expenses['Category'].unique():
            cat_data = expenses[expenses['Category'] == category]
            category_details.append({
                'category': category,
                'total': cat_data['Abs_Amount'].sum(),
                'count': len(cat_data),
                'avg': cat_data['Abs_Amount'].mean(),
                'transactions': cat_data[['Description', 'Abs_Amount']].to_dict('records')[:3]  # Top 3
            })
        
        # Time patterns
        hourly_spending = expenses.groupby(expenses['Date'].dt.hour)['Abs_Amount'].sum().to_dict() if not expenses.empty else {}
        daily_spending = expenses.groupby(expenses['Date'].dt.day_name())['Abs_Amount'].sum().to_dict() if not expenses.empty else {}
        
        # Budget vs actual detailed breakdown
        budget_details = []
        for category, data in budget.items():
            if isinstance(data, dict):
                budget_details.append(f"- {category}: ${data.get('actual', 0):.2f} spent vs ${data.get('budget', 0):.2f} budget ({data.get('percentage_used', 0):.1f}% used)")
        
        return {
            'total_spent': stats.get('total_spent', 0),
            'transaction_count': len(df),
            'expense_count': len(expenses),
            'category_count': len(expenses['Category'].unique()) if not expenses.empty else 0,
            'category_details': json.dumps(category_details, indent=2),
            'budget_breakdown': '\n'.join(budget_details),
            'largest_expense': expenses['Abs_Amount'].max() if not expenses.empty else 0,
            'smallest_expense': expenses['Abs_Amount'].min() if not expenses.empty else 0,
            'avg_transaction': expenses['Abs_Amount'].mean() if not expenses.empty else 0,
            'spending_patterns': json.dumps({'hourly': hourly_spending, 'daily': daily_spending}, indent=2),
            'top_merchants': expenses['Description'].value_counts().head(5).to_dict() if not expenses.empty else {},
            'date_range': f"{df['Date'].min()} to {df['Date'].max()}" if not df.empty else "No data"
        }
    
    def _get_empty_context(self) -> Dict:
        """Return empty context for when no data is available"""
        return {
            'total_spent': 0, 'transaction_count': 0, 'expense_count': 0,
            'category_count': 0, 'category_details': '[]', 'budget_breakdown': 'No budget data',
            'largest_expense': 0, 'smallest_expense': 0, 'avg_transaction': 0,
            'spending_patterns': '{}', 'top_merchants': {}, 'date_range': 'No data'
        }
    
    def _get_comprehensive_template(self) -> str:
        return """Use zen consensus with gemini-pro and o3 to analyze my comprehensive spending data:

FINANCIAL OVERVIEW:
- Total Spent: ${total_spent:.2f} across {transaction_count} transactions
- {expense_count} expenses across {category_count} categories
- Average transaction: ${avg_transaction:.2f}
- Largest expense: ${largest_expense:.2f}

DETAILED CATEGORY BREAKDOWN:
{category_details}

BUDGET ANALYSIS:
{budget_breakdown}

SPENDING PATTERNS:
{spending_patterns}

ANALYSIS REQUEST:
I need both models to provide deep insights on:
1. Overall financial discipline and health
2. Category-specific spending patterns and anomalies
3. Budget adherence and areas for improvement
4. Behavioral patterns in my spending
5. Actionable strategies for optimization

Please provide specific, quantified recommendations with priority levels."""
    
    def _get_budget_template(self) -> str:
        return """Use zen thinkdeep with gemini-pro to analyze my budget performance:

BUDGET VS ACTUAL ANALYSIS:
{budget_breakdown}

SPENDING CONTEXT:
- Total spent: ${total_spent:.2f} 
- Transaction count: {transaction_count}
- Category distribution: {category_count} categories

DETAILED CATEGORY DATA:
{category_details}

DEEP ANALYSIS REQUEST:
I need extended reasoning about:
1. Which budget categories are most problematic and why
2. Root cause analysis of overspending patterns
3. Budget reallocation strategies
4. Psychological factors affecting my spending decisions
5. Long-term budget optimization plan

Provide multi-step reasoning with specific dollar amounts and timeline recommendations."""
    
    def _get_behavioral_template(self) -> str:
        return """Use zen analyze with o3 to examine my spending behavior patterns:

BEHAVIORAL DATA:
- Spending patterns: {spending_patterns}
- Top merchants: {top_merchants}
- Transaction frequency: {transaction_count} transactions
- Average spending: ${avg_transaction:.2f}

CATEGORY BEHAVIOR:
{category_details}

BEHAVIORAL ANALYSIS REQUEST:
Analyze my spending behavior focusing on:
1. Time-based spending patterns (daily/hourly trends)
2. Merchant loyalty and repeat spending habits
3. Impulse vs planned spending indicators
4. Emotional spending triggers
5. Habit formation opportunities

Provide behavioral insights with specific improvement strategies."""
    
    def _get_predictive_template(self) -> str:
        return """Use zen consensus with gemini-pro and flash to predict my future spending:

CURRENT SPENDING DATA:
- Daily average: ${avg_transaction:.2f}
- Category distribution: {category_count} categories
- Recent period: {date_range}

DETAILED SPENDING:
{category_details}

PREDICTIVE ANALYSIS REQUEST:
Both models should predict:
1. Next week's likely spending by category
2. Month-end budget risk assessment  
3. Seasonal spending trend predictions
4. Financial goal impact projections
5. Early warning indicators to watch

Include probability estimates and risk factors for each prediction."""
    
    def _get_optimization_template(self) -> str:
        return """Use zen planner with gemini-pro to create my spending optimization plan:

OPTIMIZATION BASELINE:
- Current spending: ${total_spent:.2f}
- Budget performance: {budget_breakdown}
- Category breakdown: {category_details}

OPTIMIZATION PLANNING REQUEST:
Create a step-by-step plan for:
1. Immediate cost reduction opportunities (next 7 days)
2. Medium-term spending habit changes (next 30 days)  
3. Long-term financial optimization (next 90 days)
4. Budget rebalancing strategy
5. Tracking and accountability system

Provide specific action items with dollar impact estimates and difficulty ratings."""


if __name__ == "__main__":
    # Test enhanced analysis
    analyzer = EnhancedAIAnalyzer()
    
    # Mock data for testing
    mock_stats = {'total_spent': 150.75, 'transaction_count': 8}
    mock_budget = {'Food': {'actual': 75.50, 'budget': 100.00, 'percentage_used': 75.5}}
    
    prompts = analyzer.generate_enhanced_analysis_prompts(pd.DataFrame(), mock_budget, mock_stats)
    
    print("🤖 ENHANCED AI ANALYSIS PROMPTS GENERATED:")
    for analysis_type, prompt in prompts.items():
        print(f"\n📊 {analysis_type.upper()}:")
        print("-" * 50)
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)