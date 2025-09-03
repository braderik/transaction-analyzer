"""
Specialized AI Analysis Roles for Enhanced Financial Insights
Based on multi-model consensus recommendations for Phase 2 enhancements
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json
from dataclasses import dataclass


@dataclass
class RiskAssessment:
    """Risk assessment data structure"""
    risk_level: str
    confidence: float
    factors: List[str]
    recommendations: List[str]
    severity_score: int  # 0-100


@dataclass
class GrowthOpportunity:
    """Growth opportunity data structure"""
    category: str
    opportunity_type: str  # 'savings', 'optimization', 'automation'
    potential_value: float
    effort_level: str  # 'low', 'medium', 'high'
    timeframe: str  # 'immediate', 'short_term', 'long_term'
    action_items: List[str]


class RiskOfficerAnalysis:
    """Specialized AI role: Financial Risk Officer
    
    Focuses on identifying financial risks, compliance issues,
    and protective strategies for financial health.
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'high_volatility': 100.0,  # Daily spending variance
            'concentration_risk': 0.4,  # % of spending in one category
            'trend_deterioration': 20.0,  # % increase in spending trend
            'emergency_fund_ratio': 0.1,  # Below 10% of monthly spending
            'debt_service_ratio': 0.3   # Above 30% of income
        }
    
    def assess_financial_risks(self, transaction_data: pd.DataFrame, 
                             analysis_results: Dict) -> RiskAssessment:
        """Comprehensive financial risk assessment"""
        
        risk_factors = []
        recommendations = []
        severity_scores = []
        
        # 1. Spending Volatility Risk
        volatility_risk = self._assess_spending_volatility(transaction_data)
        if volatility_risk['is_risk']:
            risk_factors.append(f"High spending volatility: {volatility_risk['score']:.1f}")
            recommendations.extend(volatility_risk['recommendations'])
            severity_scores.append(volatility_risk['severity'])
        
        # 2. Category Concentration Risk
        concentration_risk = self._assess_category_concentration(transaction_data)
        if concentration_risk['is_risk']:
            risk_factors.append(f"Over-concentrated in {concentration_risk['category']}: {concentration_risk['percentage']:.1f}%")
            recommendations.extend(concentration_risk['recommendations'])
            severity_scores.append(concentration_risk['severity'])
        
        # 3. Trend Deterioration Risk
        trend_risk = self._assess_spending_trends(analysis_results)
        if trend_risk['is_risk']:
            risk_factors.append(f"Negative spending trend: {trend_risk['trend_description']}")
            recommendations.extend(trend_risk['recommendations'])
            severity_scores.append(trend_risk['severity'])
        
        # 4. Liquidity Risk Assessment
        liquidity_risk = self._assess_liquidity_risk(analysis_results)
        if liquidity_risk['is_risk']:
            risk_factors.append(f"Liquidity concern: {liquidity_risk['description']}")
            recommendations.extend(liquidity_risk['recommendations'])
            severity_scores.append(liquidity_risk['severity'])
        
        # 5. Behavioral Risk Patterns
        behavioral_risk = self._assess_behavioral_patterns(transaction_data)
        if behavioral_risk['is_risk']:
            risk_factors.append(f"Behavioral pattern risk: {behavioral_risk['pattern']}")
            recommendations.extend(behavioral_risk['recommendations'])
            severity_scores.append(behavioral_risk['severity'])
        
        # Calculate overall risk level
        overall_severity = max(severity_scores) if severity_scores else 0
        risk_level = self._determine_overall_risk_level(overall_severity, len(risk_factors))
        confidence = min(95.0, 60.0 + (len(risk_factors) * 10))  # Higher confidence with more factors
        
        return RiskAssessment(
            risk_level=risk_level,
            confidence=confidence,
            factors=risk_factors,
            recommendations=recommendations,
            severity_score=overall_severity
        )
    
    def _assess_spending_volatility(self, df: pd.DataFrame) -> Dict:
        """Assess spending volatility risk"""
        if df.empty or len(df) < 7:
            return {'is_risk': False, 'severity': 0}
        
        expenses = df[df['Is_Expense']].copy()
        daily_spending = expenses.groupby(expenses['Date'].dt.date)['Abs_Amount'].sum()
        
        if len(daily_spending) < 3:
            return {'is_risk': False, 'severity': 0}
        
        volatility = daily_spending.std()
        mean_spending = daily_spending.mean()
        coefficient_of_variation = (volatility / mean_spending) if mean_spending > 0 else 0
        
        is_high_risk = volatility > self.risk_thresholds['high_volatility']
        severity = min(100, int(coefficient_of_variation * 100))
        
        return {
            'is_risk': is_high_risk,
            'score': volatility,
            'severity': severity,
            'recommendations': [
                "📊 Implement daily spending budgets to reduce volatility",
                "🎯 Set up spending alerts for unusual transaction amounts",
                "📅 Create a weekly spending plan to smooth out daily variations"
            ] if is_high_risk else []
        }
    
    def _assess_category_concentration(self, df: pd.DataFrame) -> Dict:
        """Assess category concentration risk"""
        if df.empty:
            return {'is_risk': False, 'severity': 0}
        
        expenses = df[df['Is_Expense']].copy()
        category_totals = expenses.groupby('Category')['Abs_Amount'].sum()
        total_spending = category_totals.sum()
        
        if total_spending == 0:
            return {'is_risk': False, 'severity': 0}
        
        max_category = category_totals.idxmax()
        max_percentage = (category_totals.max() / total_spending)
        
        is_concentrated = max_percentage > self.risk_thresholds['concentration_risk']
        severity = min(100, int(max_percentage * 150))  # Scale to 0-100
        
        return {
            'is_risk': is_concentrated,
            'category': max_category,
            'percentage': max_percentage * 100,
            'severity': severity,
            'recommendations': [
                f"💰 Diversify spending away from {max_category}",
                "🔍 Review if high {max_category} spending is necessary",
                "📋 Set stricter limits for over-concentrated categories"
            ] if is_concentrated else []
        }
    
    def _assess_spending_trends(self, analysis_results: Dict) -> Dict:
        """Assess negative spending trend risks"""
        trend_analysis = analysis_results.get('trend_analysis', {})
        category_trends = trend_analysis.get('category_trends', {})
        
        deteriorating_categories = []
        total_negative_slope = 0
        
        for category, trend_data in category_trends.items():
            if trend_data.get('trend_direction') == 'increasing':
                slope = trend_data.get('trend_slope', 0)
                if slope > 10:  # Increasing by more than $10/day trend
                    deteriorating_categories.append({
                        'category': category,
                        'slope': slope,
                        'daily_average': trend_data.get('average_daily', 0)
                    })
                    total_negative_slope += slope
        
        is_risk = len(deteriorating_categories) >= 2 or total_negative_slope > 50
        severity = min(100, int(total_negative_slope))
        
        return {
            'is_risk': is_risk,
            'trend_description': f"{len(deteriorating_categories)} categories trending upward",
            'severity': severity,
            'recommendations': [
                f"📈 Address increasing spending in {cat['category']}" 
                for cat in deteriorating_categories[:3]
            ] + [
                "🎯 Implement trend-based spending alerts",
                "📊 Review monthly to catch negative trends early"
            ] if is_risk else []
        }
    
    def _assess_liquidity_risk(self, analysis_results: Dict) -> Dict:
        """Assess liquidity and cash flow risks"""
        cash_flow = analysis_results.get('cash_flow_health', {})
        net_flow = cash_flow.get('net_cash_flow', 0)
        expense_ratio = cash_flow.get('expense_to_income_ratio', 0)
        
        # Risk factors
        negative_cash_flow = net_flow < 0
        high_expense_ratio = expense_ratio > 0.9  # Spending >90% of income
        
        is_risk = negative_cash_flow or high_expense_ratio
        severity = 0
        
        if negative_cash_flow:
            severity += 50
        if high_expense_ratio:
            severity += int((expense_ratio - 0.7) * 100)  # Scale based on how high
        
        severity = min(100, severity)
        
        return {
            'is_risk': is_risk,
            'description': f"Expense ratio: {expense_ratio:.1%}, Net flow: ${net_flow:.2f}",
            'severity': severity,
            'recommendations': [
                "🚨 Immediate expense reduction needed - negative cash flow",
                "💰 Build emergency fund to 3-6 months expenses",
                "📊 Track cash flow weekly until positive",
                "🎯 Target expense ratio below 80% of income"
            ] if is_risk else []
        }
    
    def _assess_behavioral_patterns(self, df: pd.DataFrame) -> Dict:
        """Assess risky behavioral spending patterns"""
        if df.empty:
            return {'is_risk': False, 'severity': 0}
        
        expenses = df[df['Is_Expense']].copy()
        risky_patterns = []
        severity = 0
        
        # Weekend overspending pattern
        weekend_spending = expenses[expenses['Date'].dt.weekday >= 5]['Abs_Amount'].sum()
        weekday_spending = expenses[expenses['Date'].dt.weekday < 5]['Abs_Amount'].sum()
        
        if weekend_spending > 0 and weekday_spending > 0:
            weekend_ratio = weekend_spending / (weekend_spending + weekday_spending)
            if weekend_ratio > 0.4:  # >40% on weekends
                risky_patterns.append(f"High weekend spending: {weekend_ratio:.1%}")
                severity += 30
        
        # Late night spending (if time data available)
        if 'Date' in expenses.columns:
            try:
                late_night_transactions = 0
                for _, transaction in expenses.iterrows():
                    if hasattr(transaction['Date'], 'hour'):
                        if transaction['Date'].hour >= 22 or transaction['Date'].hour <= 6:
                            late_night_transactions += 1
                
                if late_night_transactions > len(expenses) * 0.2:  # >20% late night
                    risky_patterns.append("Frequent late-night spending")
                    severity += 20
            except:
                pass  # Time data not available or not properly formatted
        
        # Impulse buying patterns (multiple small transactions same day)
        daily_transaction_counts = expenses.groupby(expenses['Date'].dt.date).size()
        high_transaction_days = (daily_transaction_counts > 5).sum()
        
        if high_transaction_days > len(daily_transaction_counts) * 0.3:
            risky_patterns.append("Frequent multiple daily transactions")
            severity += 25
        
        is_risk = len(risky_patterns) > 0
        pattern_description = "; ".join(risky_patterns)
        
        return {
            'is_risk': is_risk,
            'pattern': pattern_description,
            'severity': min(100, severity),
            'recommendations': [
                "🛑 Implement 24-hour waiting period for non-essential purchases",
                "📱 Use spending apps with real-time alerts",
                "🎯 Set specific times for shopping to avoid impulse buying",
                "💡 Review triggers that lead to overspending patterns"
            ] if is_risk else []
        }
    
    def _determine_overall_risk_level(self, max_severity: int, risk_factor_count: int) -> str:
        """Determine overall risk level based on severity and factor count"""
        if max_severity >= 80 or risk_factor_count >= 4:
            return "High Risk"
        elif max_severity >= 60 or risk_factor_count >= 3:
            return "Moderate Risk"
        elif max_severity >= 40 or risk_factor_count >= 2:
            return "Low Risk"
        elif risk_factor_count >= 1:
            return "Minimal Risk"
        else:
            return "Low Risk"


class GrowthStrategistAnalysis:
    """Specialized AI role: Financial Growth Strategist
    
    Focuses on optimization opportunities, efficiency improvements,
    and strategic financial growth initiatives.
    """
    
    def __init__(self):
        self.optimization_categories = {
            'subscriptions': {'priority': 'high', 'potential_savings': 0.15},
            'dining': {'priority': 'medium', 'potential_savings': 0.25},
            'transportation': {'priority': 'medium', 'potential_savings': 0.20},
            'shopping': {'priority': 'high', 'potential_savings': 0.30},
            'utilities': {'priority': 'low', 'potential_savings': 0.10}
        }
    
    def identify_growth_opportunities(self, transaction_data: pd.DataFrame, 
                                   analysis_results: Dict) -> List[GrowthOpportunity]:
        """Identify comprehensive growth and optimization opportunities"""
        
        opportunities = []
        
        # 1. Subscription Optimization
        sub_opportunities = self._identify_subscription_optimization(transaction_data)
        opportunities.extend(sub_opportunities)
        
        # 2. Spending Efficiency Improvements
        efficiency_opportunities = self._identify_efficiency_improvements(transaction_data)
        opportunities.extend(efficiency_opportunities)
        
        # 3. Automation Opportunities
        automation_opportunities = self._identify_automation_opportunities(analysis_results)
        opportunities.extend(automation_opportunities)
        
        # 4. Behavioral Optimization
        behavioral_opportunities = self._identify_behavioral_optimizations(transaction_data)
        opportunities.extend(behavioral_opportunities)
        
        # 5. Strategic Financial Moves
        strategic_opportunities = self._identify_strategic_opportunities(analysis_results)
        opportunities.extend(strategic_opportunities)
        
        # Sort by potential value
        opportunities.sort(key=lambda x: x.potential_value, reverse=True)
        
        return opportunities
    
    def _identify_subscription_optimization(self, df: pd.DataFrame) -> List[GrowthOpportunity]:
        """Identify subscription optimization opportunities"""
        opportunities = []
        
        if df.empty:
            return opportunities
        
        expenses = df[df['Is_Expense']].copy()
        
        # Look for recurring subscription-like patterns
        recurring_vendors = expenses.groupby('Description').agg({
            'Abs_Amount': ['count', 'mean', 'std'],
            'Date': ['min', 'max']
        }).round(2)
        
        # Filter for potential subscriptions (low variance, multiple occurrences)
        potential_subscriptions = []
        for vendor in recurring_vendors.index:
            count = recurring_vendors.loc[vendor, ('Abs_Amount', 'count')]
            std_dev = recurring_vendors.loc[vendor, ('Abs_Amount', 'std')]
            mean_amount = recurring_vendors.loc[vendor, ('Abs_Amount', 'mean')]
            
            if count >= 2 and std_dev < (mean_amount * 0.1):  # Low variance
                potential_subscriptions.append({
                    'vendor': vendor,
                    'monthly_cost': mean_amount * 4,  # Approximate monthly
                    'frequency': count
                })
        
        # Create optimization opportunities
        for sub in potential_subscriptions:
            opportunities.append(GrowthOpportunity(
                category="Subscription Management",
                opportunity_type="optimization",
                potential_value=sub['monthly_cost'] * 0.3,  # 30% potential savings
                effort_level="low",
                timeframe="immediate",
                action_items=[
                    f"Review {sub['vendor']} subscription necessity",
                    f"Compare pricing with alternatives",
                    f"Consider annual vs monthly billing for discounts",
                    f"Set calendar reminder to review in 6 months"
                ]
            ))
        
        return opportunities
    
    def _identify_efficiency_improvements(self, df: pd.DataFrame) -> List[GrowthOpportunity]:
        """Identify spending efficiency improvements"""
        opportunities = []
        
        if df.empty:
            return opportunities
        
        expenses = df[df['Is_Expense']].copy()
        category_spending = expenses.groupby('Category')['Abs_Amount'].sum().sort_values(ascending=False)
        
        # Focus on top spending categories
        for category in category_spending.head(3).index:
            category_expenses = expenses[expenses['Category'] == category]
            total_spent = category_expenses['Abs_Amount'].sum()
            
            # Different strategies per category
            if category in ['Shopping', 'Food & Dining', 'Entertainment']:
                opportunities.append(GrowthOpportunity(
                    category=f"{category} Efficiency",
                    opportunity_type="savings",
                    potential_value=total_spent * 0.2,  # 20% potential savings
                    effort_level="medium",
                    timeframe="short_term",
                    action_items=[
                        f"Set monthly {category} budget with weekly check-ins",
                        f"Use cash-back credit cards for {category} purchases",
                        f"Research discount apps and loyalty programs",
                        f"Implement 24-hour waiting period for non-essential {category} items"
                    ]
                ))
            
            elif category == 'Transportation':
                opportunities.append(GrowthOpportunity(
                    category="Transportation Optimization",
                    opportunity_type="optimization",
                    potential_value=total_spent * 0.25,  # 25% potential savings
                    effort_level="medium",
                    timeframe="short_term",
                    action_items=[
                        "Compare rideshare vs public transit costs",
                        "Consider transportation subscription services",
                        "Plan trips to reduce total transportation needs",
                        "Explore carpooling or bike-sharing options"
                    ]
                ))
        
        return opportunities
    
    def _identify_automation_opportunities(self, analysis_results: Dict) -> List[GrowthOpportunity]:
        """Identify financial automation opportunities"""
        opportunities = []
        
        # Automated savings opportunity
        cash_flow = analysis_results.get('cash_flow_health', {})
        net_flow = cash_flow.get('net_cash_flow', 0)
        
        if net_flow > 100:  # Positive cash flow
            automated_savings_amount = net_flow * 0.5  # Save 50% of excess
            
            opportunities.append(GrowthOpportunity(
                category="Automated Savings",
                opportunity_type="automation",
                potential_value=automated_savings_amount * 12,  # Annual value
                effort_level="low",
                timeframe="immediate",
                action_items=[
                    f"Set up automatic transfer of ${automated_savings_amount:.2f} to savings",
                    "Use high-yield savings account for emergency fund",
                    "Consider automated investment in index funds",
                    "Set up automatic bill pay to avoid late fees"
                ]
            ))
        
        # Budget automation
        opportunities.append(GrowthOpportunity(
            category="Budget Automation",
            opportunity_type="automation",
            potential_value=200,  # Value in time and avoided overspending
            effort_level="low",
            timeframe="immediate",
            action_items=[
                "Set up automatic spending alerts at 80% of budget",
                "Use budgeting apps with bank integration",
                "Automate categorization of recurring transactions",
                "Set up weekly spending summary emails"
            ]
        ))
        
        return opportunities
    
    def _identify_behavioral_optimizations(self, df: pd.DataFrame) -> List[GrowthOpportunity]:
        """Identify behavioral optimization opportunities"""
        opportunities = []
        
        if df.empty:
            return opportunities
        
        expenses = df[df['Is_Expense']].copy()
        
        # Timing-based optimizations
        day_patterns = expenses.groupby(expenses['Date'].dt.day_name())['Abs_Amount'].sum()
        if not day_patterns.empty:
            highest_day = day_patterns.idxmax()
            highest_amount = day_patterns.max()
            
            if highest_amount > day_patterns.mean() * 1.5:  # 50% above average
                opportunities.append(GrowthOpportunity(
                    category="Spending Pattern Optimization",
                    opportunity_type="optimization",
                    potential_value=highest_amount * 0.3 * 4,  # Monthly potential savings
                    effort_level="medium",
                    timeframe="short_term",
                    action_items=[
                        f"Plan {highest_day} spending in advance to avoid impulse purchases",
                        f"Set specific {highest_day} spending limit",
                        "Use shopping lists and stick to them",
                        "Consider online shopping with cart delays"
                    ]
                ))
        
        return opportunities
    
    def _identify_strategic_opportunities(self, analysis_results: Dict) -> List[GrowthOpportunity]:
        """Identify strategic financial opportunities"""
        opportunities = []
        
        # Cash flow optimization
        cash_flow = analysis_results.get('cash_flow_health', {})
        savings_rate = cash_flow.get('savings_rate', 0)
        
        if savings_rate < 20:  # Below recommended 20% savings rate
            opportunities.append(GrowthOpportunity(
                category="Savings Rate Improvement",
                opportunity_type="optimization",
                potential_value=1000,  # Strategic value
                effort_level="high",
                timeframe="long_term",
                action_items=[
                    f"Increase savings rate from {savings_rate:.1f}% to 20%",
                    "Identify largest expense categories for reduction",
                    "Consider income-increasing activities",
                    "Implement zero-based budgeting approach"
                ]
            ))
        
        # Investment opportunity (if significant positive cash flow)
        net_flow = cash_flow.get('net_cash_flow', 0)
        if net_flow > 500:  # Significant positive cash flow
            opportunities.append(GrowthOpportunity(
                category="Investment Growth",
                opportunity_type="automation",
                potential_value=net_flow * 0.07 * 12,  # 7% annual return estimate
                effort_level="medium",
                timeframe="long_term",
                action_items=[
                    f"Invest ${net_flow * 0.3:.2f} monthly in diversified index funds",
                    "Open tax-advantaged accounts (IRA, 401k)",
                    "Consider robo-advisor for automated investing",
                    "Review and rebalance portfolio quarterly"
                ]
            ))
        
        return opportunities


def generate_specialized_analysis_report(risk_assessment: RiskAssessment, 
                                       growth_opportunities: List[GrowthOpportunity]) -> str:
    """Generate comprehensive specialized analysis report"""
    
    report = f"""
🎯 SPECIALIZED AI ANALYSIS REPORT
==================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🛡️ RISK OFFICER ASSESSMENT
==========================
Overall Risk Level: {risk_assessment.risk_level}
Confidence: {risk_assessment.confidence:.1f}%
Risk Score: {risk_assessment.severity_score}/100

📊 Risk Factors Identified:
"""
    
    for i, factor in enumerate(risk_assessment.factors, 1):
        report += f"{i}. {factor}\n"
    
    if not risk_assessment.factors:
        report += "✅ No significant risk factors identified\n"
    
    report += "\n🛡️ Risk Mitigation Recommendations:\n"
    for i, rec in enumerate(risk_assessment.recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += f"""

📈 GROWTH STRATEGIST OPPORTUNITIES
===================================
Total Opportunities Identified: {len(growth_opportunities)}
"""
    
    # Group opportunities by timeframe
    immediate_ops = [op for op in growth_opportunities if op.timeframe == 'immediate']
    short_term_ops = [op for op in growth_opportunities if op.timeframe == 'short_term']
    long_term_ops = [op for op in growth_opportunities if op.timeframe == 'long_term']
    
    total_potential_value = sum(op.potential_value for op in growth_opportunities)
    
    report += f"Total Potential Annual Value: ${total_potential_value:.2f}\n\n"
    
    # Immediate opportunities
    if immediate_ops:
        report += "🚀 IMMEDIATE OPPORTUNITIES (0-30 days):\n"
        for i, op in enumerate(immediate_ops, 1):
            report += f"{i}. {op.category} - ${op.potential_value:.2f} potential value\n"
            report += f"   Effort: {op.effort_level.title()}\n"
            for action in op.action_items[:2]:  # Show first 2 actions
                report += f"   • {action}\n"
            report += "\n"
    
    # Short-term opportunities
    if short_term_ops:
        report += "📅 SHORT-TERM OPPORTUNITIES (1-6 months):\n"
        for i, op in enumerate(short_term_ops, 1):
            report += f"{i}. {op.category} - ${op.potential_value:.2f} potential value\n"
            report += f"   Effort: {op.effort_level.title()}\n"
            for action in op.action_items[:2]:  # Show first 2 actions
                report += f"   • {action}\n"
            report += "\n"
    
    # Long-term opportunities
    if long_term_ops:
        report += "🎯 LONG-TERM OPPORTUNITIES (6+ months):\n"
        for i, op in enumerate(long_term_ops, 1):
            report += f"{i}. {op.category} - ${op.potential_value:.2f} potential value\n"
            report += f"   Effort: {op.effort_level.title()}\n"
            for action in op.action_items[:2]:  # Show first 2 actions
                report += f"   • {action}\n"
            report += "\n"
    
    report += """
🎯 NEXT STEPS
=============
1. Address any High Risk factors immediately
2. Implement immediate opportunities (low effort, high value first)
3. Plan short-term opportunities with specific timelines
4. Set up systems for long-term opportunities
5. Review and adjust monthly

📊 This analysis uses advanced pattern recognition and strategic
   financial principles to provide actionable insights for your
   financial optimization and risk management.
"""
    
    return report


if __name__ == "__main__":
    # Test with sample data
    print("Testing Specialized AI Analysis Roles...")
    
    # This would normally be called from the main workflow
    sample_data = pd.DataFrame({
        'Date': pd.to_datetime(['2025-01-29'] * 5),
        'Description': ['Netflix Subscription', 'Starbucks Coffee', 'Uber Ride', 'Amazon Purchase', 'Grocery Store'],
        'Amount': [-12.99, -5.50, -15.00, -45.99, -23.50],
        'Category': ['Entertainment', 'Food & Dining', 'Transportation', 'Shopping', 'Food & Dining'],
        'Is_Expense': [True] * 5,
        'Abs_Amount': [12.99, 5.50, 15.00, 45.99, 23.50]
    })
    
    # Test Risk Officer
    risk_officer = RiskOfficerAnalysis()
    mock_analysis = {
        'cash_flow_health': {'net_cash_flow': 500, 'expense_to_income_ratio': 0.7},
        'trend_analysis': {'category_trends': {'Shopping': {'trend_direction': 'increasing', 'trend_slope': 15}}}
    }
    
    risk_assessment = risk_officer.assess_financial_risks(sample_data, mock_analysis)
    
    # Test Growth Strategist
    growth_strategist = GrowthStrategistAnalysis()
    opportunities = growth_strategist.identify_growth_opportunities(sample_data, mock_analysis)
    
    # Generate report
    report = generate_specialized_analysis_report(risk_assessment, opportunities)
    print(report)