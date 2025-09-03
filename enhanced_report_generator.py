"""
Enhanced HTML Report Generator with Specialized AI Analysis
"""
from datetime import datetime
from typing import Dict, Any
import json


class EnhancedReportGenerator:
    """Generate enhanced HTML reports with specialized AI analysis"""
    
    def __init__(self):
        self.report_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Financial Analysis - {target_date}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .summary-box {{ background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .alert-high {{ background: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; }}
        .alert-medium {{ background: #fff8e1; border-left: 4px solid #ff9800; padding: 15px; margin: 10px 0; }}
        .alert-low {{ background: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; }}
        .risk-section {{ background: #ffe6e6; border-left: 4px solid #dc3545; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .growth-section {{ background: #e6f7ff; border-left: 4px solid #1890ff; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .opportunity {{ background: #f0f9ff; border: 1px solid #e0f2fe; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .chart-container {{ text-align: center; margin: 30px 0; }}
        .chart-container img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #3498db; color: white; border-radius: 8px; min-width: 150px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; }}
        .metric-label {{ font-size: 14px; }}
        .metric-risk {{ background: #dc3545; }}
        .metric-growth {{ background: #28a745; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        .recommendations {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .zen-section {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #9c27b0; }}
        .progress-bar {{ width: 100%; background-color: #f0f0f0; border-radius: 10px; margin: 5px 0; }}
        .progress-fill {{ height: 20px; background-color: #4caf50; border-radius: 10px; text-align: center; line-height: 20px; color: white; font-size: 12px; }}
        .risk-high {{ background-color: #dc3545; }}
        .risk-moderate {{ background-color: #ffc107; }}
        .risk-low {{ background-color: #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Enhanced Financial Analysis Report</h1>
        <p><strong>Analysis Date:</strong> {analysis_date}</p>
        <p><strong>Target Date:</strong> {target_date}</p>
        <p><strong>Generated:</strong> {generated_at}</p>
        
        <div class="summary-box">
            <h2>🏆 Executive Summary</h2>
            {executive_summary}
        </div>
        
        <div class="summary-box">
            <h2>📈 Key Metrics</h2>
            {key_metrics}
        </div>
        
        {risk_analysis_section}
        
        {growth_opportunities_section}
        
        <h2>📊 Visual Analysis</h2>
        {visual_analysis}
        
        <h2>⚠️ Alerts & Recommendations</h2>
        {alerts_recommendations}
        
        <div class="zen-section">
            <h2>🤖 AI Analysis with Zen MCP</h2>
            {zen_analysis}
        </div>
        
        <h2>📋 Detailed Analysis</h2>
        {detailed_analysis}
        
        <div class="summary-box">
            <h2>🎯 Next Steps</h2>
            {next_steps}
        </div>
    </div>
</body>
</html>
"""
    
    def generate_enhanced_report(self, analysis_results: Dict[str, Any], 
                               output_path: str = None) -> str:
        """Generate enhanced HTML report with specialized AI analysis"""
        
        # Extract data from analysis results
        metadata = analysis_results.get('metadata', {})
        daily_summary = analysis_results.get('daily_summary', {})
        specialized_analysis = analysis_results.get('specialized_ai_analysis', {})
        
        # Generate report sections
        executive_summary = self._generate_executive_summary(daily_summary)
        key_metrics = self._generate_key_metrics(analysis_results)
        risk_analysis_section = self._generate_risk_analysis_section(specialized_analysis)
        growth_opportunities_section = self._generate_growth_opportunities_section(specialized_analysis)
        visual_analysis = self._generate_visual_analysis_section()
        alerts_recommendations = self._generate_alerts_recommendations_section(analysis_results)
        zen_analysis = self._generate_zen_analysis_section(analysis_results)
        detailed_analysis = self._generate_detailed_analysis_section(analysis_results)
        next_steps = self._generate_next_steps_section(specialized_analysis)
        
        # Fill in the template
        html_content = self.report_template.format(
            analysis_date=metadata.get('analysis_date', 'Unknown'),
            target_date=metadata.get('target_date', 'Unknown'),
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            executive_summary=executive_summary,
            key_metrics=key_metrics,
            risk_analysis_section=risk_analysis_section,
            growth_opportunities_section=growth_opportunities_section,
            visual_analysis=visual_analysis,
            alerts_recommendations=alerts_recommendations,
            zen_analysis=zen_analysis,
            detailed_analysis=detailed_analysis,
            next_steps=next_steps
        )
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return html_content
    
    def _generate_executive_summary(self, daily_summary: Dict) -> str:
        """Generate executive summary HTML"""
        basic_summary = daily_summary.get('basic_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        
        total_spent = basic_summary.get('total_spent', 0)
        transaction_count = daily_summary.get('transaction_count', 0)
        risk_level = overspending.get('risk_level', 'Unknown')
        spending_score = overspending.get('spending_score', 0)
        
        risk_color = self._get_risk_color(risk_level)
        
        return f"""
        <p><strong>Total Spent:</strong> ${total_spent:.2f}</p>
        <p><strong>Number of Transactions:</strong> {transaction_count}</p>
        <p><strong>Risk Level:</strong> <span style="color: {risk_color};">{risk_level}</span></p>
        <p><strong>Spending Score:</strong> {spending_score}/100</p>
        """
    
    def _generate_key_metrics(self, analysis_results: Dict) -> str:
        """Generate key metrics HTML"""
        daily_summary = analysis_results.get('daily_summary', {})
        specialized_analysis = analysis_results.get('specialized_ai_analysis', {})
        trend_analysis = analysis_results.get('trend_analysis', {})
        
        total_spent = daily_summary.get('basic_summary', {}).get('total_spent', 0)
        potential_savings = analysis_results.get('opportunity_analysis', {}).get('total_potential_savings', 0)
        vs_average = trend_analysis.get('yesterday_vs_average', {}).get('percentage_change', 0)
        
        # Specialized metrics
        risk_score = specialized_analysis.get('risk_assessment', {}).get('severity_score', 0)
        total_opportunity_value = specialized_analysis.get('total_opportunity_value', 0)
        high_priority_ops = specialized_analysis.get('high_priority_opportunities', 0)
        
        return f"""
        <div class="metric"><div class="metric-value">${total_spent:.2f}</div><div class="metric-label">Total Spent</div></div>
        <div class="metric"><div class="metric-value">${potential_savings:.2f}</div><div class="metric-label">Potential Savings</div></div>
        <div class="metric"><div class="metric-value">{vs_average:+.1f}%</div><div class="metric-label">vs Weekly Average</div></div>
        <div class="metric metric-risk"><div class="metric-value">{risk_score}/100</div><div class="metric-label">Risk Score</div></div>
        <div class="metric metric-growth"><div class="metric-value">${total_opportunity_value:.0f}</div><div class="metric-label">Growth Opportunities</div></div>
        <div class="metric"><div class="metric-value">{high_priority_ops}</div><div class="metric-label">High Priority Actions</div></div>
        """
    
    def _generate_risk_analysis_section(self, specialized_analysis: Dict) -> str:
        """Generate risk analysis section"""
        risk_assessment = specialized_analysis.get('risk_assessment', {})
        
        if not risk_assessment:
            return ""
        
        risk_level = risk_assessment.get('risk_level', 'Unknown')
        confidence = risk_assessment.get('confidence', 0)
        severity_score = risk_assessment.get('severity_score', 0)
        factors = risk_assessment.get('factors', [])
        recommendations = risk_assessment.get('recommendations', [])
        
        factors_html = ""
        for i, factor in enumerate(factors, 1):
            factors_html += f"<li>{factor}</li>"
        
        recommendations_html = ""
        for i, rec in enumerate(recommendations, 1):
            recommendations_html += f"<li>{rec}</li>"
        
        return f"""
        <div class="risk-section">
            <h2>🛡️ Risk Officer Analysis</h2>
            <div class="progress-bar">
                <div class="progress-fill risk-{self._get_risk_level_class(risk_level)}" style="width: {severity_score}%;">
                    Risk Score: {severity_score}/100
                </div>
            </div>
            <p><strong>Overall Risk Level:</strong> {risk_level}</p>
            <p><strong>Assessment Confidence:</strong> {confidence:.1f}%</p>
            
            <h3>🚨 Risk Factors Identified:</h3>
            <ul>{factors_html}</ul>
            
            <h3>🛡️ Risk Mitigation Recommendations:</h3>
            <ul>{recommendations_html}</ul>
        </div>
        """
    
    def _generate_growth_opportunities_section(self, specialized_analysis: Dict) -> str:
        """Generate growth opportunities section"""
        opportunities = specialized_analysis.get('growth_opportunities', [])
        total_value = specialized_analysis.get('total_opportunity_value', 0)
        
        if not opportunities:
            return ""
        
        # Group by timeframe
        immediate_ops = [op for op in opportunities if op['timeframe'] == 'immediate']
        short_term_ops = [op for op in opportunities if op['timeframe'] == 'short_term']
        long_term_ops = [op for op in opportunities if op['timeframe'] == 'long_term']
        
        def format_opportunities(ops_list, title):
            if not ops_list:
                return ""
            
            html = f"<h3>{title}</h3>"
            for op in ops_list:
                actions_html = ""
                for action in op['action_items'][:3]:  # Show first 3 actions
                    actions_html += f"<li>{action}</li>"
                
                html += f"""
                <div class="opportunity">
                    <h4>{op['category']} - ${op['potential_value']:.2f} potential value</h4>
                    <p><strong>Type:</strong> {op['opportunity_type'].title()} | 
                       <strong>Effort:</strong> {op['effort_level'].title()}</p>
                    <ul>{actions_html}</ul>
                </div>
                """
            return html
        
        opportunities_html = ""
        opportunities_html += format_opportunities(immediate_ops, "🚀 Immediate Opportunities (0-30 days)")
        opportunities_html += format_opportunities(short_term_ops, "📅 Short-term Opportunities (1-6 months)")
        opportunities_html += format_opportunities(long_term_ops, "🎯 Long-term Opportunities (6+ months)")
        
        return f"""
        <div class="growth-section">
            <h2>📈 Growth Strategist Opportunities</h2>
            <p><strong>Total Opportunities:</strong> {len(opportunities)}</p>
            <p><strong>Total Potential Annual Value:</strong> ${total_value:.2f}</p>
            
            {opportunities_html}
        </div>
        """
    
    def _generate_visual_analysis_section(self) -> str:
        """Generate visual analysis section"""
        return """
        <div class="chart-container">
            <h3>Spending by Category</h3>
            <img src="charts/category_spending_2025-07-29.png" alt="Spending by Category">
        </div>
        
        <div class="chart-container">
            <h3>Budget vs Actual</h3>
            <img src="charts/budget_comparison_2025-07-29.png" alt="Budget vs Actual">
        </div>
        
        <div class="chart-container">
            <h3>Spending Trends</h3>
            <img src="charts/spending_trends_2025-07-29.png" alt="Spending Trends">
        </div>
        """
    
    def _generate_alerts_recommendations_section(self, analysis_results: Dict) -> str:
        """Generate alerts and recommendations section"""
        daily_summary = analysis_results.get('daily_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        recommendations = overspending.get('recommendations', [])
        
        rec_html = ""
        for rec in recommendations:
            rec_html += f"<li>{rec}</li>"
        
        return f"""
        <div class="recommendations">
            <h3>💡 Recommendations</h3>
            <ul>{rec_html}</ul>
        </div>
        """
    
    def _generate_zen_analysis_section(self, analysis_results: Dict) -> str:
        """Generate Zen MCP analysis section"""
        return """
        <p>🚀 <strong>Ready for AI-Powered Analysis!</strong></p>
        <p>Use the following prompts in Claude Code CLI with Zen MCP for deep insights:</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #9c27b0;">
            <strong>🤖 Consensus Analysis Prompt:</strong><br>
            <em>Copy this into Claude Code CLI:</em><br><br>
            <code style="white-space: pre-wrap; font-size: 12px;">Use zen consensus to analyze my spending patterns and get perspectives from both gemini pro and o3 on where I'm overspending and actionable advice.</code>
        </div>
        
        <p><strong>Available Zen Tools for Your Analysis:</strong></p>
        <ul>
            <li><strong>consensus</strong> - Get multiple AI perspectives on your spending</li>
            <li><strong>analyze</strong> - Deep analysis of spending patterns</li>
            <li><strong>debug</strong> - Systematic investigation of overspending issues</li>
            <li><strong>thinkdeep</strong> - Extended reasoning about financial habits</li>
        </ul>
        """
    
    def _generate_detailed_analysis_section(self, analysis_results: Dict) -> str:
        """Generate detailed analysis section"""
        return """
        <p>Complete transaction breakdown, trend analysis, and predictive forecasting available in JSON results.</p>
        """
    
    def _generate_next_steps_section(self, specialized_analysis: Dict) -> str:
        """Generate next steps section"""
        risk_assessment = specialized_analysis.get('risk_assessment', {})
        high_priority_ops = specialized_analysis.get('high_priority_opportunities', 0)
        
        return f"""
        <br>🎯 <strong>Priority Actions:</strong><br>
        • Address {len(risk_assessment.get('factors', []))} risk factors identified
        • Implement {high_priority_ops} high-priority opportunities
        • Run specialized AI analysis weekly for optimization
        • Set up automated alerts for risk monitoring
        <br><br>
        🤖 <strong>Enhanced Analysis:</strong><br>
        • Risk Officer identified potential financial risks
        • Growth Strategist found optimization opportunities
        • Combined analysis provides actionable insights
        """
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level"""
        colors = {
            'Excellent': 'green',
            'Good': 'lightgreen',
            'Fair': 'orange',
            'Poor': 'red',
            'Critical': 'darkred',
            'High Risk': 'red',
            'Moderate Risk': 'orange',
            'Low Risk': 'green',
            'Minimal Risk': 'lightgreen'
        }
        return colors.get(risk_level, 'gray')
    
    def _get_risk_level_class(self, risk_level: str) -> str:
        """Get CSS class for risk level"""
        if 'High' in risk_level or 'Critical' in risk_level:
            return 'high'
        elif 'Moderate' in risk_level or 'Fair' in risk_level:
            return 'moderate'
        else:
            return 'low'


if __name__ == "__main__":
    # Test the enhanced report generator
    print("Enhanced Report Generator ready for integration!")