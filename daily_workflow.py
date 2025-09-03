"""
Automated Daily Transaction Analysis Workflow
Implementing comprehensive financial analysis with Zen MCP integration
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json
import os
from transaction_retriever import TransactionRetriever
from zen_analyzer import ZenAnalyzer, BudgetAnalyzer
from overspending_analyzer import OverspendingAnalyzer
from specialized_ai_roles import RiskOfficerAnalysis, GrowthStrategistAnalysis, generate_specialized_analysis_report
from enhanced_report_generator import EnhancedReportGenerator
import config


class DailyWorkflowAnalyzer:
    """Comprehensive daily financial analysis workflow"""
    
    def __init__(self):
        self.retriever = TransactionRetriever()
        self.zen_analyzer = ZenAnalyzer()
        self.budget_analyzer = BudgetAnalyzer()
        self.overspending_analyzer = OverspendingAnalyzer()
        self.risk_officer = RiskOfficerAnalysis()
        self.growth_strategist = GrowthStrategistAnalysis()
        self.report_generator = EnhancedReportGenerator()
        self.today = datetime.now()
        self.yesterday = self.today - timedelta(days=1)
    
    def run_daily_analysis(self) -> Dict[str, Any]:
        """Run complete daily analysis workflow"""
        print("🚀 Starting Daily Transaction Analysis...")
        
        # Connect to Google Sheets
        if not self.retriever.connect():
            return {"error": "Failed to connect to Google Sheets"}
        
        # Get transaction data
        yesterday_data = self.retriever.get_previous_day_transactions(self.yesterday)
        week_data = self.retriever.get_date_range_transactions(
            self.today - timedelta(days=7), self.today
        )
        month_data = self.retriever.get_date_range_transactions(
            self.today - timedelta(days=30), self.today
        )
        
        # Run all analysis components
        analysis_results = {
            'metadata': {
                'analysis_date': self.today.strftime('%Y-%m-%d'),
                'target_date': self.yesterday.strftime('%Y-%m-%d'),
                'generated_at': datetime.now().isoformat()
            },
            'daily_summary': self._analyze_daily_summary(yesterday_data),
            'trend_analysis': self._analyze_trends_and_variance(yesterday_data, week_data),
            'predictive_forecasting': self._analyze_predictive_spend(month_data),
            'vendor_analysis': self._analyze_vendors_and_categories(week_data),
            'comparative_benchmarks': self._analyze_comparative_benchmarks(yesterday_data),
            'opportunity_analysis': self._analyze_opportunities(yesterday_data, week_data),
            'budget_sensitivity': self._analyze_budget_scenarios(month_data),
            'alerting_habits': self._analyze_habits_and_alerts(yesterday_data, week_data),
            'data_hygiene': self._analyze_data_classification(yesterday_data),
            'cash_flow_health': self._analyze_cash_flow_health(week_data),
            'zen_ai_analysis': self._generate_ai_insights(yesterday_data)
        }
        
        # Run specialized AI analysis after the main analysis is complete
        analysis_results['specialized_ai_analysis'] = self._run_specialized_ai_analysis(yesterday_data, week_data, analysis_results)
        
        # Generate comprehensive report
        report = self._generate_daily_report(analysis_results)
        analysis_results['daily_report'] = report
        
        return analysis_results
    
    def _convert_to_json_safe(self, df_or_series) -> Dict:
        """Convert pandas DataFrame/Series to JSON-safe dictionary"""
        try:
            if hasattr(df_or_series, 'to_dict'):
                result = df_or_series.to_dict()
                # Convert any remaining non-serializable types
                return json.loads(json.dumps(result, default=str))
            return df_or_series
        except:
            return str(df_or_series)
    
    def _analyze_daily_summary(self, df: pd.DataFrame) -> Dict:
        """1. Basic daily summary with overspending analysis"""
        if df.empty:
            return {"status": "no_data", "message": "No transactions found for yesterday"}
        
        summary = self.retriever.get_spending_summary(df)
        overspending = self.overspending_analyzer.analyze_daily_overspending(df)
        
        return {
            "basic_summary": summary,
            "overspending_analysis": overspending,
            "transaction_count": len(df),
            "expense_count": len(df[df['Is_Expense']]),
            "largest_expense": {
                "amount": float(df[df['Is_Expense']]['Abs_Amount'].max()) if not df[df['Is_Expense']].empty else 0,
                "description": df.loc[df[df['Is_Expense']]['Abs_Amount'].idxmax(), 'Description'] if not df[df['Is_Expense']].empty else "N/A"
            }
        }
    
    def _analyze_trends_and_variance(self, daily_df: pd.DataFrame, week_df: pd.DataFrame) -> Dict:
        """2. Trend & Variance Analysis"""
        if week_df.empty:
            return {"status": "insufficient_data"}
        
        expenses = week_df[week_df['Is_Expense']].copy()
        
        # Calculate daily averages
        daily_avg = expenses.groupby(expenses['Date'].dt.date)['Abs_Amount'].sum().mean()
        yesterday_total = daily_df[daily_df['Is_Expense']]['Abs_Amount'].sum() if not daily_df.empty else 0
        
        # Category trends
        category_trends = {}
        for category in expenses['Category'].unique():
            cat_data = expenses[expenses['Category'] == category]
            daily_cat_spending = cat_data.groupby(cat_data['Date'].dt.date)['Abs_Amount'].sum()
            
            if len(daily_cat_spending) > 1:
                trend_slope = np.polyfit(range(len(daily_cat_spending)), daily_cat_spending.values, 1)[0]
                category_trends[category] = {
                    'average_daily': float(daily_cat_spending.mean()),
                    'trend_direction': 'increasing' if trend_slope > 1 else 'decreasing' if trend_slope < -1 else 'stable',
                    'variance': float(daily_cat_spending.var()),
                    'trend_slope': float(trend_slope)
                }
        
        return {
            "weekly_average_daily": float(daily_avg),
            "yesterday_vs_average": {
                "amount": float(yesterday_total),
                "difference": float(yesterday_total - daily_avg),
                "percentage_change": float(((yesterday_total - daily_avg) / daily_avg * 100)) if daily_avg > 0 else 0
            },
            "category_trends": category_trends,
            "volatility_score": float(expenses.groupby(expenses['Date'].dt.date)['Abs_Amount'].sum().std())
        }
    
    def _analyze_predictive_spend(self, month_df: pd.DataFrame) -> Dict:
        """3. Predictive Spend Forecasting"""
        if month_df.empty:
            return {"status": "insufficient_data"}
        
        expenses = month_df[month_df['Is_Expense']].copy()
        days_in_period = (datetime.now() - (datetime.now() - timedelta(days=30))).days
        days_remaining_in_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - datetime.now()
        days_remaining_in_month = days_remaining_in_month.days
        
        # Calculate daily spending rate
        daily_spending_rate = expenses['Abs_Amount'].sum() / days_in_period
        
        # Forecast by category
        category_forecasts = {}
        for category in expenses['Category'].unique():
            cat_spending = expenses[expenses['Category'] == category]['Abs_Amount'].sum()
            daily_cat_rate = cat_spending / days_in_period
            projected_month_total = daily_cat_rate * 30  # Assuming 30-day month
            budget_limit = config.DAILY_BUDGET_LIMITS.get(category, 0) * 30
            
            category_forecasts[category] = {
                'current_spend': float(cat_spending),
                'daily_rate': float(daily_cat_rate),
                'projected_month_total': float(projected_month_total),
                'budget_limit': float(budget_limit),
                'projected_over_budget': float(projected_month_total - budget_limit) if budget_limit > 0 else 0,
                'will_exceed_budget': projected_month_total > budget_limit if budget_limit > 0 else False
            }
        
        return {
            "daily_spending_rate": float(daily_spending_rate),
            "projected_month_total": float(daily_spending_rate * 30),
            "days_remaining_in_month": days_remaining_in_month,
            "category_forecasts": category_forecasts,
            "high_risk_categories": [cat for cat, data in category_forecasts.items() if data['will_exceed_budget']]
        }
    
    def _analyze_vendors_and_categories(self, week_df: pd.DataFrame) -> Dict:
        """4. Category & Vendor Deep Dive"""
        if week_df.empty:
            return {"status": "insufficient_data"}
        
        expenses = week_df[week_df['Is_Expense']].copy()
        
        # Top vendors analysis
        vendor_spending = expenses.groupby('Description').agg({
            'Abs_Amount': ['sum', 'count', 'mean']
        }).round(2)
        vendor_spending.columns = ['total_spent', 'transaction_count', 'avg_amount']
        top_vendors = vendor_spending.nlargest(10, 'total_spent')
        
        # Convert to JSON-safe format
        top_vendors_dict = {}
        for vendor, row in top_vendors.iterrows():
            top_vendors_dict[str(vendor)] = {
                'total_spent': float(row['total_spent']),
                'transaction_count': int(row['transaction_count']),
                'avg_amount': float(row['avg_amount'])
            }
        
        # Detect recurring patterns
        recurring_vendors = expenses.groupby('Description').filter(lambda x: len(x) >= 2)
        recurring_analysis = recurring_vendors.groupby('Description').agg({
            'Abs_Amount': ['sum', 'count', 'std'],
            'Date': lambda x: (x.max() - x.min()).days
        }).round(2)
        
        return {
            "top_vendors": top_vendors_dict,
            "recurring_vendors": self._convert_to_json_safe(recurring_analysis),
            "category_breakdown": self._convert_to_json_safe(expenses.groupby('Category')['Abs_Amount'].agg(['sum', 'count', 'mean'])),
            "subscription_candidates": [vendor for vendor in recurring_analysis.index 
                                     if recurring_analysis.loc[vendor, ('Abs_Amount', 'std')] < 5]  # Low variance suggests subscription
        }
    
    def _analyze_comparative_benchmarks(self, daily_df: pd.DataFrame) -> Dict:
        """5. Comparative Benchmarks"""
        if daily_df.empty:
            return {"status": "no_data"}
        
        # Hardcoded benchmark data (could be expanded with real data sources)
        us_average_daily_spending = {
            'Food & Dining': 35.0,
            'Transportation': 25.0,
            'Shopping': 30.0,
            'Entertainment': 15.0,
            'Healthcare': 20.0,
            'Utilities': 12.0
        }
        
        expenses = daily_df[daily_df['Is_Expense']].copy()
        category_spending = expenses.groupby('Category')['Abs_Amount'].sum()
        
        comparisons = {}
        for category, spent in category_spending.items():
            benchmark = us_average_daily_spending.get(category, 0)
            if benchmark > 0:
                comparisons[category] = {
                    'your_spending': float(spent),
                    'us_average': float(benchmark),
                    'difference': float(spent - benchmark),
                    'percentage_vs_average': float((spent / benchmark) * 100),
                    'above_average': spent > benchmark
                }
        
        return {
            "category_comparisons": comparisons,
            "overall_vs_average": {
                "your_total": float(expenses['Abs_Amount'].sum()),
                "estimated_us_average": float(sum(us_average_daily_spending.values())),
                "percentage_vs_average": float((expenses['Abs_Amount'].sum() / sum(us_average_daily_spending.values())) * 100)
            }
        }
    
    def _analyze_opportunities(self, daily_df: pd.DataFrame, week_df: pd.DataFrame) -> Dict:
        """6. Opportunity Analysis"""
        opportunities = []
        
        if not daily_df.empty:
            expenses = daily_df[daily_df['Is_Expense']].copy()
            
            # High-spending categories
            category_totals = expenses.groupby('Category')['Abs_Amount'].sum()
            for category, amount in category_totals.items():
                budget = config.DAILY_BUDGET_LIMITS.get(category, 0)
                if budget > 0 and amount > budget:
                    savings_potential = amount - budget
                    opportunities.append({
                        'type': 'reduce_category_spending',
                        'category': category,
                        'current_spend': float(amount),
                        'target_spend': float(budget),
                        'potential_savings': float(savings_potential),
                        'action': f"Reduce {category} spending by ${savings_potential:.2f}",
                        'priority': 'High' if savings_potential > 20 else 'Medium'
                    })
        
        if not week_df.empty:
            week_expenses = week_df[week_df['Is_Expense']].copy()
            
            # Subscription optimization
            recurring_vendors = week_expenses.groupby('Description').filter(lambda x: len(x) >= 2)
            for vendor in recurring_vendors['Description'].unique():
                vendor_data = recurring_vendors[recurring_vendors['Description'] == vendor]
                if vendor_data['Abs_Amount'].std() < 2:  # Consistent amounts suggest subscription
                    opportunities.append({
                        'type': 'subscription_review',
                        'vendor': vendor,
                        'monthly_cost': float(vendor_data['Abs_Amount'].mean() * 4),  # Approximate monthly
                        'action': f"Review {vendor} subscription - cancel if unused",
                        'potential_savings': float(vendor_data['Abs_Amount'].mean() * 4),
                        'priority': 'Medium'
                    })
        
        return {
            "opportunities": opportunities,
            "total_potential_savings": sum(opp.get('potential_savings', 0) for opp in opportunities),
            "high_priority_count": len([opp for opp in opportunities if opp.get('priority') == 'High'])
        }
    
    def _analyze_budget_scenarios(self, month_df: pd.DataFrame) -> Dict:
        """7. Budget Sensitivity / What-If Analysis"""
        if month_df.empty:
            return {"status": "insufficient_data"}
        
        expenses = month_df[month_df['Is_Expense']].copy()
        current_monthly = expenses['Abs_Amount'].sum()
        
        scenarios = {
            "reduce_dining_10": {
                "description": "Reduce Food & Dining by 10%",
                "savings": float(expenses[expenses['Category'] == 'Food & Dining']['Abs_Amount'].sum() * 0.1),
                "new_total": 0
            },
            "reduce_shopping_20": {
                "description": "Reduce Shopping by 20%",
                "savings": float(expenses[expenses['Category'] == 'Shopping']['Abs_Amount'].sum() * 0.2),
                "new_total": 0
            },
            "eliminate_entertainment": {
                "description": "Eliminate Entertainment spending",
                "savings": float(expenses[expenses['Category'] == 'Entertainment']['Abs_Amount'].sum()),
                "new_total": 0
            }
        }
        
        for scenario in scenarios.values():
            scenario["new_total"] = float(current_monthly - scenario["savings"])
            scenario["percentage_reduction"] = float((scenario["savings"] / current_monthly) * 100)
        
        return {
            "current_monthly_spend": float(current_monthly),
            "scenarios": scenarios,
            "best_savings_scenario": max(scenarios.keys(), key=lambda k: scenarios[k]["savings"])
        }
    
    def _analyze_habits_and_alerts(self, daily_df: pd.DataFrame, week_df: pd.DataFrame) -> Dict:
        """8. Alerting & Habit Analysis"""
        alerts = []
        habits = {}
        
        if not daily_df.empty:
            overspending = self.overspending_analyzer.analyze_daily_overspending(daily_df)
            
            # Generate alerts from overspending analysis
            for alert in overspending.get('overspending_alerts', []):
                alerts.append({
                    'type': 'overspending',
                    'category': alert['category'],
                    'severity': alert['severity'],
                    'message': f"{alert['category']} spending is {alert['percentage_used']:.0f}% of budget"
                })
        
        if not week_df.empty:
            # Analyze spending patterns by day of week
            week_expenses = week_df[week_df['Is_Expense']].copy()
            day_patterns = week_expenses.groupby(week_expenses['Date'].dt.day_name())['Abs_Amount'].agg(['sum', 'count'])
            
            habits = {
                "day_of_week_patterns": self._convert_to_json_safe(day_patterns),
                "highest_spending_day": day_patterns['sum'].idxmax() if not day_patterns.empty else None,
                "most_transactions_day": day_patterns['count'].idxmax() if not day_patterns.empty else None
            }
        
        return {
            "alerts": alerts,
            "habits": habits,
            "alert_count": len(alerts),
            "habit_insights": self._generate_habit_insights(habits)
        }
    
    def _analyze_data_classification(self, daily_df: pd.DataFrame) -> Dict:
        """9. Transaction Classification / Data Hygiene"""
        if daily_df.empty:
            return {"status": "no_data"}
        
        # Find uncategorized or miscellaneous transactions
        uncategorized = daily_df[daily_df['Category'].isin(['Miscellaneous', '', 'Other'])]
        
        # Find potentially mislabeled transactions
        suspicious_transactions = []
        for _, transaction in daily_df.iterrows():
            description = transaction['Description'].lower()
            category = transaction['Category']
            
            # Check for obvious mismatches
            if 'starbucks' in description and category != 'Food & Dining':
                suspicious_transactions.append({
                    'description': transaction['Description'],
                    'current_category': category,
                    'suggested_category': 'Food & Dining',
                    'amount': float(transaction['Abs_Amount']) if transaction['Is_Expense'] else float(transaction['Amount'])
                })
        
        return {
            "uncategorized_count": len(uncategorized),
            "uncategorized_transactions": uncategorized[['Description', 'Amount', 'Category']].to_dict('records'),
            "suspicious_transactions": suspicious_transactions,
            "data_quality_score": float(((len(daily_df) - len(uncategorized)) / len(daily_df)) * 100) if len(daily_df) > 0 else 100
        }
    
    def _analyze_cash_flow_health(self, week_df: pd.DataFrame) -> Dict:
        """10. Cash Flow Health Check"""
        if week_df.empty:
            return {"status": "insufficient_data"}
        
        expenses = week_df[week_df['Is_Expense']].copy()
        income = week_df[~week_df['Is_Expense']].copy()
        
        total_expenses = expenses['Abs_Amount'].sum()
        total_income = income['Amount'].sum()
        net_cash_flow = total_income - total_expenses
        
        # Analyze by account type (if available)
        account_analysis = {}
        if 'Account' in week_df.columns:
            account_breakdown = expenses.groupby('Account')['Abs_Amount'].sum()
            account_analysis = self._convert_to_json_safe(account_breakdown)
        
        return {
            "weekly_expenses": float(total_expenses),
            "weekly_income": float(total_income),
            "net_cash_flow": float(net_cash_flow),
            "expense_to_income_ratio": float(total_expenses / total_income) if total_income > 0 else 0,
            "account_breakdown": account_analysis,
            "cash_flow_health": "Positive" if net_cash_flow > 0 else "Negative",
            "savings_rate": float(net_cash_flow / total_income * 100) if total_income > 0 else 0
        }
    
    def _generate_ai_insights(self, daily_df: pd.DataFrame) -> Dict:
        """Generate AI analysis prompts for Zen MCP"""
        if daily_df.empty:
            return {"status": "no_data"}
        
        summary = self.retriever.get_spending_summary(daily_df)
        zen_analyses = self.zen_analyzer.generate_comprehensive_analysis(daily_df, summary)
        
        return zen_analyses
    
    def _run_specialized_ai_analysis(self, daily_df: pd.DataFrame, week_df: pd.DataFrame, 
                                   analysis_results: Dict) -> Dict:
        """Run specialized AI analysis with Risk Officer and Growth Strategist"""
        if daily_df.empty and week_df.empty:
            return {"status": "no_data"}
        
        print("🤖 Running Specialized AI Analysis...")
        
        # Combine daily and weekly data for comprehensive analysis
        combined_df = pd.concat([daily_df, week_df]).drop_duplicates()
        
        # Risk Officer Analysis
        risk_assessment = self.risk_officer.assess_financial_risks(combined_df, analysis_results)
        
        # Growth Strategist Analysis  
        growth_opportunities = self.growth_strategist.identify_growth_opportunities(combined_df, analysis_results)
        
        # Generate specialized report
        specialized_report = generate_specialized_analysis_report(risk_assessment, growth_opportunities)
        
        return {
            'risk_assessment': {
                'risk_level': risk_assessment.risk_level,
                'confidence': risk_assessment.confidence,
                'severity_score': risk_assessment.severity_score,
                'factors': risk_assessment.factors,
                'recommendations': risk_assessment.recommendations
            },
            'growth_opportunities': [
                {
                    'category': op.category,
                    'opportunity_type': op.opportunity_type,
                    'potential_value': op.potential_value,
                    'effort_level': op.effort_level,
                    'timeframe': op.timeframe,
                    'action_items': op.action_items
                }
                for op in growth_opportunities
            ],
            'total_opportunity_value': sum(op.potential_value for op in growth_opportunities),
            'high_priority_opportunities': len([op for op in growth_opportunities if op.effort_level == 'low' and op.potential_value > 100]),
            'specialized_report': specialized_report
        }
    
    def _generate_habit_insights(self, habits: Dict) -> List[str]:
        """Generate insights from habit analysis"""
        insights = []
        
        if habits.get("day_of_week_patterns"):
            patterns = habits["day_of_week_patterns"]
            highest_day = habits.get("highest_spending_day")
            
            if highest_day:
                insights.append(f"You tend to spend most on {highest_day}s")
            
            # Check for weekend spending
            weekend_spending = patterns.get('Saturday', {}).get('sum', 0) + patterns.get('Sunday', {}).get('sum', 0)
            weekday_avg = sum(patterns.get(day, {}).get('sum', 0) for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']) / 5
            
            if weekend_spending > weekday_avg * 2:
                insights.append("Weekend spending is significantly higher than weekdays")
        
        return insights
    
    def _generate_daily_report(self, analysis_results: Dict) -> str:
        """Generate comprehensive daily report"""
        report = f"""
📊 DAILY FINANCIAL ANALYSIS REPORT
=================================
Generated: {analysis_results['metadata']['analysis_date']}
Analysis Period: {analysis_results['metadata']['target_date']}

🏆 EXECUTIVE SUMMARY
===================
"""
        
        # Add summary based on analysis results
        daily_summary = analysis_results.get('daily_summary', {})
        if daily_summary.get('basic_summary'):
            total_spent = daily_summary['basic_summary'].get('total_spent', 0)
            report += f"Total Spent Yesterday: ${total_spent:.2f}\n"
            report += f"Number of Transactions: {daily_summary.get('transaction_count', 0)}\n"
            
            overspending = daily_summary.get('overspending_analysis', {})
            risk_level = overspending.get('risk_level', 'Unknown')
            report += f"Spending Risk Level: {risk_level}\n"
        
        # Add key insights
        report += "\n🎯 KEY INSIGHTS\n===============\n"
        
        # Trend analysis
        trends = analysis_results.get('trend_analysis', {})
        if trends.get('yesterday_vs_average'):
            change = trends['yesterday_vs_average'].get('percentage_change', 0)
            if abs(change) > 10:
                direction = "higher" if change > 0 else "lower"
                report += f"• Yesterday's spending was {abs(change):.1f}% {direction} than your weekly average\n"
        
        # Opportunities
        opportunities = analysis_results.get('opportunity_analysis', {})
        total_savings = opportunities.get('total_potential_savings', 0)
        if total_savings > 0:
            report += f"• Potential savings identified: ${total_savings:.2f}\n"
        
        # Alerts
        alerts = analysis_results.get('alerting_habits', {})
        alert_count = alerts.get('alert_count', 0)
        if alert_count > 0:
            report += f"• {alert_count} spending alerts require attention\n"
        
        # Add specialized AI analysis section
        specialized_analysis = analysis_results.get('specialized_ai_analysis', {})
        if specialized_analysis.get('specialized_report'):
            report += "\n" + specialized_analysis['specialized_report']
        
        # Add AI analysis section
        report += "\n🤖 ADDITIONAL AI ANALYSIS READY\n==============================\n"
        report += "Use the following prompts in Claude Code CLI with Zen MCP:\n\n"
        
        ai_analysis = analysis_results.get('zen_ai_analysis', {})
        if ai_analysis.get('consensus_prompt'):
            report += "CONSENSUS ANALYSIS:\n"
            report += ai_analysis['consensus_prompt']
            report += "\n\n"
        
        return report


if __name__ == "__main__":
    # Run the daily workflow
    workflow = DailyWorkflowAnalyzer()
    results = workflow.run_daily_analysis()
    
    # Save results to file
    output_file = f"/Users/bradyswanson2/transaction-analyzer/daily_analysis_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("✅ Daily analysis complete!")
    print(f"📄 Results saved to: {output_file}")
    
    # Print the daily report
    if 'daily_report' in results:
        print("\n" + results['daily_report'])