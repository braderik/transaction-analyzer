"""
Advanced Overspending Analysis with Pattern Detection
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import config


class OverspendingAnalyzer:
    """Advanced analysis of spending patterns and overspending detection"""
    
    def __init__(self):
        self.budget_limits = config.DAILY_BUDGET_LIMITS
        self.overspending_threshold = config.OVERSPENDING_THRESHOLD
        self.warning_threshold = config.WARNING_THRESHOLD
    
    def analyze_daily_overspending(self, df: pd.DataFrame) -> Dict:
        """Analyze overspending for a specific day"""
        if df.empty:
            return self._empty_analysis()
        
        expenses = df[df['Is_Expense']].copy()
        
        # Calculate spending by category
        category_spending = expenses.groupby('Category')['Abs_Amount'].sum()
        
        analysis = {
            'date': df['Date'].iloc[0].strftime('%Y-%m-%d') if not df.empty else 'Unknown',
            'total_spent': float(expenses['Abs_Amount'].sum()),
            'total_transactions': len(expenses),
            'categories_analyzed': len(category_spending),
            'overspending_alerts': [],
            'warning_alerts': [],
            'within_budget': [],
            'recommendations': [],
            'spending_score': 0,  # 0-100 scale
            'risk_level': 'Unknown'
        }
        
        total_budget = sum(self.budget_limits.values())
        budget_used_percentage = (analysis['total_spent'] / total_budget) * 100 if total_budget > 0 else 0
        
        # Analyze each category
        for category, spent in category_spending.items():
            budget_limit = self.budget_limits.get(category, 0)
            
            if budget_limit == 0:
                continue
            
            percentage_used = (spent / budget_limit) * 100
            over_amount = spent - budget_limit
            
            category_analysis = {
                'category': category,
                'spent': float(spent),
                'budget': float(budget_limit),
                'percentage_used': float(percentage_used),
                'over_amount': float(over_amount),
                'transaction_count': int(len(expenses[expenses['Category'] == category]))
            }
            
            # Categorize spending level
            if percentage_used >= (self.overspending_threshold * 100):
                category_analysis['status'] = 'OVERSPENDING'
                category_analysis['severity'] = self._calculate_severity(percentage_used)
                analysis['overspending_alerts'].append(category_analysis)
                
            elif percentage_used >= (self.warning_threshold * 100):
                category_analysis['status'] = 'WARNING'
                category_analysis['severity'] = 'Medium'
                analysis['warning_alerts'].append(category_analysis)
                
            else:
                category_analysis['status'] = 'WITHIN_BUDGET'
                category_analysis['savings'] = float(budget_limit - spent)
                analysis['within_budget'].append(category_analysis)
        
        # Calculate overall spending score and risk level
        analysis['spending_score'] = self._calculate_spending_score(analysis)
        analysis['risk_level'] = self._determine_risk_level(analysis['spending_score'])
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def analyze_spending_trends(self, df: pd.DataFrame, days: int = 7) -> Dict:
        """Analyze spending trends over multiple days"""
        if df.empty:
            return {}
        
        # Group by date
        daily_spending = df[df['Is_Expense']].groupby(df['Date'].dt.date).agg({
            'Abs_Amount': 'sum',
            'Description': 'count'
        }).rename(columns={'Description': 'transaction_count'})
        
        # Calculate trend metrics
        trend_analysis = {
            'period_days': len(daily_spending),
            'average_daily_spending': float(daily_spending['Abs_Amount'].mean()),
            'highest_spending_day': {
                'date': str(daily_spending['Abs_Amount'].idxmax()),
                'amount': float(daily_spending['Abs_Amount'].max())
            },
            'lowest_spending_day': {
                'date': str(daily_spending['Abs_Amount'].idxmin()),
                'amount': float(daily_spending['Abs_Amount'].min())
            },
            'spending_variance': float(daily_spending['Abs_Amount'].var()),
            'trend_direction': self._calculate_trend_direction(daily_spending['Abs_Amount']),
            'consistency_score': self._calculate_consistency_score(daily_spending['Abs_Amount'])
        }
        
        return trend_analysis
    
    def detect_unusual_transactions(self, df: pd.DataFrame) -> List[Dict]:
        """Detect unusual or potentially problematic transactions"""
        if df.empty:
            return []
        
        expenses = df[df['Is_Expense']].copy()
        unusual_transactions = []
        
        # Calculate thresholds for unusual amounts
        mean_amount = expenses['Abs_Amount'].mean()
        std_amount = expenses['Abs_Amount'].std()
        high_threshold = mean_amount + (2 * std_amount)  # 2 standard deviations
        
        for _, transaction in expenses.iterrows():
            flags = []
            
            # Check for unusually high amounts
            if transaction['Abs_Amount'] > high_threshold:
                flags.append('UNUSUALLY_HIGH_AMOUNT')
            
            # Check for duplicate transactions (same amount, same day, similar description)
            similar_transactions = expenses[
                (expenses['Abs_Amount'] == transaction['Abs_Amount']) &
                (expenses['Date'].dt.date == transaction['Date'].date()) &
                (expenses.index != transaction.name)
            ]
            
            if len(similar_transactions) > 0:
                flags.append('POTENTIAL_DUPLICATE')
            
            # Check for weekend spending in certain categories
            if transaction['Date'].weekday() >= 5:  # Saturday = 5, Sunday = 6
                if transaction['Category'] in ['Shopping', 'Entertainment']:
                    flags.append('WEEKEND_DISCRETIONARY_SPENDING')
            
            # Check for late night transactions (if timestamp available)
            transaction_hour = transaction['Date'].hour if hasattr(transaction['Date'], 'hour') else None
            if transaction_hour and (transaction_hour >= 23 or transaction_hour <= 5):
                flags.append('LATE_NIGHT_SPENDING')
            
            if flags:
                unusual_transactions.append({
                    'date': transaction['Date'].strftime('%Y-%m-%d'),
                    'description': transaction['Description'],
                    'amount': float(transaction['Abs_Amount']),
                    'category': transaction['Category'],
                    'flags': flags,
                    'severity': 'High' if 'UNUSUALLY_HIGH_AMOUNT' in flags else 'Medium'
                })
        
        return unusual_transactions
    
    def _calculate_severity(self, percentage_used: float) -> str:
        """Calculate severity level based on percentage over budget"""
        if percentage_used >= 200:  # 200% or more
            return 'Critical'
        elif percentage_used >= 150:  # 150-199%
            return 'High'
        elif percentage_used >= 120:  # 120-149%
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_spending_score(self, analysis: Dict) -> float:
        """Calculate overall spending score (0-100, higher is better)"""
        base_score = 100  # Start with perfect score
        
        # Deduct points for overspending alerts
        for alert in analysis['overspending_alerts']:
            if alert['severity'] == 'Critical':
                base_score -= 30
            elif alert['severity'] == 'High':
                base_score -= 20
            elif alert['severity'] == 'Medium':
                base_score -= 15
            else:
                base_score -= 10
        
        # Deduct points for warning alerts
        base_score -= len(analysis['warning_alerts']) * 5
        
        # Bonus points for categories within budget
        base_score += len(analysis['within_budget']) * 3
        
        # Bonus for staying significantly under total budget
        total_budget = sum(self.budget_limits.values())
        if total_budget > 0 and analysis['total_spent'] < (total_budget * 0.8):
            under_budget_bonus = min(15, int((total_budget - analysis['total_spent']) / total_budget * 20))
            base_score += under_budget_bonus
        
        return min(100, max(0, base_score))  # Clamp between 0-100
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on spending score (higher score = better)"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'
    
    def _calculate_trend_direction(self, spending_series: pd.Series) -> str:
        """Calculate if spending is trending up, down, or stable"""
        if len(spending_series) < 2:
            return 'Insufficient Data'
        
        # Simple linear regression slope
        x = np.arange(len(spending_series))
        slope = np.polyfit(x, spending_series.values, 1)[0]
        
        if slope > 5:  # Increasing by more than $5/day
            return 'Increasing'
        elif slope < -5:  # Decreasing by more than $5/day
            return 'Decreasing'
        else:
            return 'Stable'
    
    def _calculate_consistency_score(self, spending_series: pd.Series) -> float:
        """Calculate consistency score (0-100, higher is more consistent)"""
        if len(spending_series) == 0:
            return 0
        
        coefficient_of_variation = spending_series.std() / spending_series.mean()
        consistency_score = max(0, 100 - (coefficient_of_variation * 100))
        
        return float(consistency_score)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Recommendations for overspending categories
        for alert in analysis['overspending_alerts']:
            if alert['severity'] == 'Critical':
                recommendations.append(
                    f"🚨 URGENT: {alert['category']} spending is {alert['percentage_used']:.0f}% "
                    f"of budget. Consider eliminating non-essential {alert['category'].lower()} "
                    f"expenses immediately."
                )
            else:
                recommendations.append(
                    f"⚠️ Reduce {alert['category']} spending by ${alert['over_amount']:.2f} "
                    f"to stay within budget."
                )
        
        # Recommendations for warning categories
        for warning in analysis['warning_alerts']:
            recommendations.append(
                f"📊 Monitor {warning['category']} spending closely - you've used "
                f"{warning['percentage_used']:.0f}% of your budget."
            )
        
        # Positive reinforcement for good categories
        if analysis['within_budget']:
            best_category = min(analysis['within_budget'], key=lambda x: x['percentage_used'])
            recommendations.append(
                f"✅ Great job staying within budget for {best_category['category']}! "
                f"You saved ${best_category['savings']:.2f}."
            )
        
        # Overall recommendations based on risk level
        if analysis['risk_level'] == 'High Risk':
            recommendations.append(
                "🎯 Consider implementing a daily spending limit and tracking expenses in real-time."
            )
        elif analysis['risk_level'] == 'Medium Risk':
            recommendations.append(
                "💡 Review your spending categories and consider setting stricter limits for problem areas."
            )
        
        return recommendations
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'date': 'No Data',
            'total_spent': 0,
            'total_transactions': 0,
            'categories_analyzed': 0,
            'overspending_alerts': [],
            'warning_alerts': [],
            'within_budget': [],
            'recommendations': ['No transaction data available for analysis.'],
            'spending_score': 0,
            'risk_level': 'Unknown'
        }


if __name__ == "__main__":
    # Test with sample data
    from datetime import datetime
    
    sample_data = pd.DataFrame({
        'Date': pd.to_datetime(['2025-01-29'] * 5),
        'Description': ['Starbucks Coffee', 'Expensive Restaurant', 'Uber Ride', 'Amazon Purchase', 'Grocery Store'],
        'Amount': [-5.50, -85.00, -12.00, -45.99, -23.50],
        'Category': ['Food & Dining', 'Food & Dining', 'Transportation', 'Shopping', 'Food & Dining'],
        'Is_Expense': [True] * 5,
        'Abs_Amount': [5.50, 85.00, 12.00, 45.99, 23.50]
    })
    
    analyzer = OverspendingAnalyzer()
    analysis = analyzer.analyze_daily_overspending(sample_data)
    
    print("📊 OVERSPENDING ANALYSIS RESULTS")
    print("================================")
    print(f"Date: {analysis['date']}")
    print(f"Total Spent: ${analysis['total_spent']:.2f}")
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"Spending Score: {analysis['spending_score']}/100")
    
    print(f"\n🚨 Overspending Alerts: {len(analysis['overspending_alerts'])}")
    for alert in analysis['overspending_alerts']:
        print(f"  - {alert['category']}: ${alert['spent']:.2f} (${alert['over_amount']:.2f} over budget)")
    
    print(f"\n💡 Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  - {rec}")