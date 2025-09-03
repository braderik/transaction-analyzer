"""
Data Visualization and Automated Reporting System
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any
import config


class VisualizationReporter:
    """Generate charts, graphs, and automated reports"""
    
    def __init__(self):
        self.output_dir = "/Users/bradyswanson2/transaction-analyzer/reports"
        self.charts_dir = f"{self.output_dir}/charts"
        self._ensure_directories()
        
        # Set style for better-looking charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def _ensure_directories(self):
        """Create output directories if they don't exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.charts_dir, exist_ok=True)
    
    def generate_daily_charts(self, analysis_results: Dict) -> Dict[str, str]:
        """Generate all daily analysis charts"""
        chart_files = {}
        date_str = analysis_results['metadata']['target_date']
        
        # 1. Spending by Category Pie Chart
        chart_files['category_pie'] = self._create_category_pie_chart(analysis_results, date_str)
        
        # 2. Budget vs Actual Bar Chart
        chart_files['budget_comparison'] = self._create_budget_comparison_chart(analysis_results, date_str)
        
        # 3. Trend Line Chart (if trend data available)
        chart_files['spending_trends'] = self._create_trend_chart(analysis_results, date_str)
        
        # 4. Overspending Heatmap
        chart_files['overspending_heatmap'] = self._create_overspending_heatmap(analysis_results, date_str)
        
        return chart_files
    
    def _create_category_pie_chart(self, analysis_results: Dict, date_str: str) -> str:
        """Create spending by category pie chart"""
        daily_summary = analysis_results.get('daily_summary', {})
        overspending_analysis = daily_summary.get('overspending_analysis', {})
        
        # Extract category data
        categories = []
        amounts = []
        colors = []
        
        for alert in overspending_analysis.get('overspending_alerts', []):
            categories.append(alert['category'])
            amounts.append(alert['spent'])
            colors.append('#ff6b6b')  # Red for overspending
        
        for warning in overspending_analysis.get('warning_alerts', []):
            categories.append(warning['category'])
            amounts.append(warning['spent'])
            colors.append('#ffd93d')  # Yellow for warnings
        
        for within in overspending_analysis.get('within_budget', []):
            categories.append(within['category'])
            amounts.append(within['spent'])
            colors.append('#6bcf7f')  # Green for within budget
        
        if not categories:
            return None
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title(f'Spending by Category - {date_str}', fontsize=16, fontweight='bold')
        
        # Add legend
        legend_labels = ['🔴 Overspending', '🟡 Warning', '🟢 Within Budget']
        legend_colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
        plt.legend(legend_labels, loc='upper right', bbox_to_anchor=(1.2, 1))
        
        filename = f"{self.charts_dir}/category_spending_{date_str}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _create_budget_comparison_chart(self, analysis_results: Dict, date_str: str) -> str:
        """Create budget vs actual spending bar chart"""
        daily_summary = analysis_results.get('daily_summary', {})
        overspending_analysis = daily_summary.get('overspending_analysis', {})
        
        categories = []
        actual_amounts = []
        budget_amounts = []
        colors = []
        
        # Collect all categories
        all_alerts = (overspending_analysis.get('overspending_alerts', []) + 
                     overspending_analysis.get('warning_alerts', []) + 
                     overspending_analysis.get('within_budget', []))
        
        for item in all_alerts:
            categories.append(item['category'])
            actual_amounts.append(item['spent'])
            budget_amounts.append(item['budget'])
            
            # Color based on status
            if item['spent'] > item['budget'] * 1.2:  # 20% over budget
                colors.append('#ff6b6b')  # Red
            elif item['spent'] > item['budget'] * 0.8:  # 80% of budget
                colors.append('#ffd93d')  # Yellow
            else:
                colors.append('#6bcf7f')  # Green
        
        if not categories:
            return None
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        x = range(len(categories))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], budget_amounts, width, label='Budget', alpha=0.7, color='lightblue')
        bars2 = ax.bar([i + width/2 for i in x], actual_amounts, width, label='Actual', color=colors)
        
        ax.set_xlabel('Categories', fontweight='bold')
        ax.set_ylabel('Amount ($)', fontweight='bold')
        ax.set_title(f'Budget vs Actual Spending - {date_str}', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'${height:.0f}', ha='center', va='bottom', fontweight='bold')
        
        filename = f"{self.charts_dir}/budget_comparison_{date_str}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _create_trend_chart(self, analysis_results: Dict, date_str: str) -> str:
        """Create spending trend line chart"""
        trend_analysis = analysis_results.get('trend_analysis', {})
        category_trends = trend_analysis.get('category_trends', {})
        
        if not category_trends:
            return None
        
        # Create trend chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Simulate trend data (in real implementation, this would use actual historical data)
        days = list(range(7))  # Last 7 days
        
        for category, trend_data in category_trends.items():
            if trend_data['trend_direction'] == 'increasing':
                # Simulate increasing trend
                values = [trend_data['average_daily'] * (1 + i * 0.1) for i in days]
            elif trend_data['trend_direction'] == 'decreasing':
                # Simulate decreasing trend
                values = [trend_data['average_daily'] * (1 - i * 0.05) for i in days]
            else:
                # Stable trend with some variance
                values = [trend_data['average_daily'] + (i % 2 - 0.5) * 2 for i in days]
            
            ax.plot(days, values, marker='o', linewidth=2, label=category)
        
        ax.set_xlabel('Days Ago', fontweight='bold')
        ax.set_ylabel('Daily Spending ($)', fontweight='bold')
        ax.set_title(f'Spending Trends by Category - {date_str}', fontsize=16, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        filename = f"{self.charts_dir}/spending_trends_{date_str}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _create_overspending_heatmap(self, analysis_results: Dict, date_str: str) -> str:
        """Create overspending severity heatmap"""
        daily_summary = analysis_results.get('daily_summary', {})
        overspending_analysis = daily_summary.get('overspending_analysis', {})
        
        # Create data for heatmap
        categories = []
        severity_scores = []
        
        for alert in overspending_analysis.get('overspending_alerts', []):
            categories.append(alert['category'])
            # Convert percentage to severity score
            percentage = alert['percentage_used']
            if percentage >= 200:
                severity_scores.append(4)  # Critical
            elif percentage >= 150:
                severity_scores.append(3)  # High
            elif percentage >= 120:
                severity_scores.append(2)  # Medium
            else:
                severity_scores.append(1)  # Low
        
        for warning in overspending_analysis.get('warning_alerts', []):
            categories.append(warning['category'])
            severity_scores.append(0.5)  # Warning level
        
        if not categories:
            return None
        
        # Create heatmap data
        heatmap_data = pd.DataFrame({
            'Category': categories,
            'Severity': severity_scores
        })
        
        # Pivot for heatmap
        heatmap_pivot = heatmap_data.set_index('Category')['Severity'].to_frame().T
        
        # Create heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_pivot, annot=True, cmap='YlOrRd', cbar_kws={'label': 'Severity Level'},
                   fmt='.1f', linewidths=0.5)
        plt.title(f'Overspending Severity Heatmap - {date_str}', fontsize=16, fontweight='bold')
        plt.ylabel('Analysis Date', fontweight='bold')
        
        filename = f"{self.charts_dir}/overspending_heatmap_{date_str}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_html_report(self, analysis_results: Dict, chart_files: Dict[str, str]) -> str:
        """Generate comprehensive HTML report"""
        date_str = analysis_results['metadata']['target_date']
        report_filename = f"{self.output_dir}/daily_report_{date_str}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Financial Analysis - {date_str}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        h1, h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .summary-box {{ background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .alert-high {{ background: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; }}
        .alert-medium {{ background: #fff8e1; border-left: 4px solid #ff9800; padding: 15px; margin: 10px 0; }}
        .alert-low {{ background: #e8f5e8; border-left: 4px solid #4caf50; padding: 15px; margin: 10px 0; }}
        .chart-container {{ text-align: center; margin: 30px 0; }}
        .chart-container img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #3498db; color: white; border-radius: 8px; min-width: 150px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; }}
        .metric-label {{ font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        .recommendations {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .zen-section {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #9c27b0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Daily Financial Analysis Report</h1>
        <p><strong>Analysis Date:</strong> {analysis_results['metadata']['analysis_date']}</p>
        <p><strong>Target Date:</strong> {date_str}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary-box">
            <h2>🏆 Executive Summary</h2>
            {self._generate_summary_html(analysis_results)}
        </div>
        
        <div class="summary-box">
            <h2>📈 Key Metrics</h2>
            {self._generate_metrics_html(analysis_results)}
        </div>
        
        <h2>📊 Visual Analysis</h2>
        {self._generate_charts_html(chart_files)}
        
        <h2>⚠️ Alerts & Recommendations</h2>
        {self._generate_alerts_html(analysis_results)}
        
        <div class="zen-section">
            <h2>🤖 AI Analysis with Zen MCP</h2>
            {self._generate_zen_html(analysis_results)}
        </div>
        
        <h2>📋 Detailed Analysis</h2>
        {self._generate_detailed_analysis_html(analysis_results)}
        
        <div class="summary-box">
            <h2>🎯 Action Items</h2>
            {self._generate_action_items_html(analysis_results)}
        </div>
    </div>
</body>
</html>
        """
        
        with open(report_filename, 'w') as f:
            f.write(html_content)
        
        return report_filename
    
    def _generate_summary_html(self, analysis_results: Dict) -> str:
        """Generate executive summary HTML"""
        daily_summary = analysis_results.get('daily_summary', {})
        basic_summary = daily_summary.get('basic_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        
        total_spent = basic_summary.get('total_spent', 0)
        risk_level = overspending.get('risk_level', 'Unknown')
        
        return f"""
        <p><strong>Total Spent:</strong> ${total_spent:.2f}</p>
        <p><strong>Number of Transactions:</strong> {daily_summary.get('transaction_count', 0)}</p>
        <p><strong>Risk Level:</strong> <span style="color: {'red' if risk_level == 'High Risk' else 'orange' if risk_level == 'Medium Risk' else 'green'};">{risk_level}</span></p>
        <p><strong>Spending Score:</strong> {overspending.get('spending_score', 0)}/100</p>
        """
    
    def _generate_metrics_html(self, analysis_results: Dict) -> str:
        """Generate key metrics HTML"""
        daily_summary = analysis_results.get('daily_summary', {})
        opportunities = analysis_results.get('opportunity_analysis', {})
        trends = analysis_results.get('trend_analysis', {})
        
        metrics_html = ""
        
        # Total spent metric
        total_spent = daily_summary.get('basic_summary', {}).get('total_spent', 0)
        metrics_html += f'<div class="metric"><div class="metric-value">${total_spent:.2f}</div><div class="metric-label">Total Spent</div></div>'
        
        # Potential savings
        potential_savings = opportunities.get('total_potential_savings', 0)
        metrics_html += f'<div class="metric"><div class="metric-value">${potential_savings:.2f}</div><div class="metric-label">Potential Savings</div></div>'
        
        # Variance from average
        if trends.get('yesterday_vs_average'):
            variance = trends['yesterday_vs_average'].get('percentage_change', 0)
            metrics_html += f'<div class="metric"><div class="metric-value">{variance:+.1f}%</div><div class="metric-label">vs Weekly Average</div></div>'
        
        return metrics_html
    
    def _generate_charts_html(self, chart_files: Dict[str, str]) -> str:
        """Generate charts section HTML"""
        charts_html = ""
        
        chart_titles = {
            'category_pie': 'Spending by Category',
            'budget_comparison': 'Budget vs Actual',
            'spending_trends': 'Spending Trends',
            'overspending_heatmap': 'Overspending Severity'
        }
        
        for chart_key, chart_file in chart_files.items():
            if chart_file and os.path.exists(chart_file):
                chart_title = chart_titles.get(chart_key, chart_key.replace('_', ' ').title())
                # Convert absolute path to relative for HTML
                relative_path = os.path.relpath(chart_file, os.path.dirname(chart_file).replace('/charts', ''))
                charts_html += f"""
                <div class="chart-container">
                    <h3>{chart_title}</h3>
                    <img src="{relative_path}" alt="{chart_title}">
                </div>
                """
        
        return charts_html
    
    def _generate_alerts_html(self, analysis_results: Dict) -> str:
        """Generate alerts section HTML"""
        daily_summary = analysis_results.get('daily_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        
        alerts_html = ""
        
        # Overspending alerts
        for alert in overspending.get('overspending_alerts', []):
            severity_class = f"alert-{alert['severity'].lower()}"
            alerts_html += f"""
            <div class="{severity_class}">
                <strong>{alert['category']} - {alert['severity']} Alert</strong><br>
                Spent: ${alert['spent']:.2f} | Budget: ${alert['budget']:.2f} | Over by: ${alert['over_amount']:.2f}
            </div>
            """
        
        # Recommendations
        recommendations = overspending.get('recommendations', [])
        if recommendations:
            alerts_html += '<div class="recommendations"><h3>💡 Recommendations</h3><ul>'
            for rec in recommendations:
                alerts_html += f'<li>{rec}</li>'
            alerts_html += '</ul></div>'
        
        return alerts_html
    
    def _generate_zen_html(self, analysis_results: Dict) -> str:
        """Generate Zen MCP section HTML"""
        zen_analysis = analysis_results.get('zen_ai_analysis', {})
        
        zen_html = """
        <p>🚀 <strong>Ready for AI-Powered Analysis!</strong></p>
        <p>Use the following prompts in Claude Code CLI with Zen MCP for deep insights:</p>
        """
        
        if zen_analysis.get('consensus_prompt'):
            zen_html += """
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #9c27b0;">
                <strong>🤖 Consensus Analysis Prompt:</strong><br>
                <em>Copy this into Claude Code CLI:</em><br><br>
                <code style="white-space: pre-wrap; font-size: 12px;">Use zen consensus to analyze my spending patterns and get perspectives from both gemini pro and o3 on where I'm overspending and actionable advice.</code>
            </div>
            """
        
        zen_html += """
        <p><strong>Available Zen Tools for Your Analysis:</strong></p>
        <ul>
            <li><strong>consensus</strong> - Get multiple AI perspectives on your spending</li>
            <li><strong>analyze</strong> - Deep analysis of spending patterns</li>
            <li><strong>debug</strong> - Systematic investigation of overspending issues</li>
            <li><strong>thinkdeep</strong> - Extended reasoning about financial habits</li>
        </ul>
        """
        
        return zen_html
    
    def _generate_detailed_analysis_html(self, analysis_results: Dict) -> str:
        """Generate detailed analysis tables"""
        html = ""
        
        # Opportunity analysis table
        opportunities = analysis_results.get('opportunity_analysis', {}).get('opportunities', [])
        if opportunities:
            html += """
            <h3>💰 Savings Opportunities</h3>
            <table>
                <tr><th>Type</th><th>Category/Vendor</th><th>Potential Savings</th><th>Action</th><th>Priority</th></tr>
            """
            for opp in opportunities:
                html += f"""
                <tr>
                    <td>{opp.get('type', 'N/A').replace('_', ' ').title()}</td>
                    <td>{opp.get('category', opp.get('vendor', 'N/A'))}</td>
                    <td>${opp.get('potential_savings', 0):.2f}</td>
                    <td>{opp.get('action', 'N/A')}</td>
                    <td>{opp.get('priority', 'Medium')}</td>
                </tr>
                """
            html += "</table>"
        
        return html
    
    def _generate_action_items_html(self, analysis_results: Dict) -> str:
        """Generate action items section"""
        action_items = []
        
        # High priority opportunities
        opportunities = analysis_results.get('opportunity_analysis', {}).get('opportunities', [])
        high_priority = [opp for opp in opportunities if opp.get('priority') == 'High']
        
        if high_priority:
            action_items.append("🔥 <strong>Immediate Actions:</strong>")
            for opp in high_priority:
                action_items.append(f"• {opp.get('action', 'Review spending')}")
        
        # Overspending alerts
        daily_summary = analysis_results.get('daily_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        critical_alerts = [alert for alert in overspending.get('overspending_alerts', []) if alert['severity'] == 'Critical']
        
        if critical_alerts:
            action_items.append("<br>🚨 <strong>Critical Issues:</strong>")
            for alert in critical_alerts:
                action_items.append(f"• Address {alert['category']} overspending (${alert['over_amount']:.2f} over budget)")
        
        # AI analysis
        action_items.append("<br>🤖 <strong>Next Steps:</strong>")
        action_items.append("• Run Zen MCP consensus analysis for deeper insights")
        action_items.append("• Review and implement top 3 savings opportunities")
        action_items.append("• Set spending alerts for problem categories")
        
        return "<br>".join(action_items) if action_items else "No specific action items identified."


if __name__ == "__main__":
    # Test with sample data
    sample_analysis = {
        'metadata': {
            'analysis_date': '2025-01-30',
            'target_date': '2025-01-29'
        },
        'daily_summary': {
            'basic_summary': {'total_spent': 127.50},
            'transaction_count': 8,
            'overspending_analysis': {
                'spending_score': 65,
                'risk_level': 'Medium Risk',
                'overspending_alerts': [
                    {
                        'category': 'Food & Dining',
                        'spent': 75.0,
                        'budget': 50.0,
                        'over_amount': 25.0,
                        'severity': 'Medium',
                        'percentage_used': 150
                    }
                ],
                'recommendations': [
                    'Reduce Food & Dining spending by $25.00 to stay within budget',
                    'Consider meal planning to reduce restaurant expenses'
                ]
            }
        },
        'opportunity_analysis': {
            'total_potential_savings': 35.00,
            'opportunities': [
                {
                    'type': 'reduce_category_spending',
                    'category': 'Food & Dining',
                    'potential_savings': 25.00,
                    'action': 'Reduce dining out expenses',
                    'priority': 'High'
                }
            ]
        },
        'zen_ai_analysis': {
            'consensus_prompt': 'Sample consensus prompt'
        }
    }
    
    reporter = VisualizationReporter()
    chart_files = reporter.generate_daily_charts(sample_analysis)
    html_report = reporter.generate_html_report(sample_analysis, chart_files)
    
    print(f"✅ Sample report generated: {html_report}")
    print(f"📊 Charts created: {len([f for f in chart_files.values() if f])}")