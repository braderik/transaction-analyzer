"""
Main Application - Transaction Analyzer with Zen MCP Integration
Comprehensive financial analysis system with AI-powered insights
"""
import sys
import os
from datetime import datetime, timedelta
import json
import argparse
from daily_workflow import DailyWorkflowAnalyzer
from visualization_reporter import VisualizationReporter
from google_sheets_auth import setup_credentials_instructions
import config


class TransactionAnalyzerApp:
    """Main application controller"""
    
    def __init__(self):
        self.workflow_analyzer = DailyWorkflowAnalyzer()
        self.reporter = VisualizationReporter()
    
    def run_daily_analysis(self, target_date=None):
        """Run complete daily analysis workflow"""
        print("🚀 TRANSACTION ANALYZER - DAILY WORKFLOW")
        print("=" * 50)
        print(f"🎯 Analysis Target: {target_date or 'Yesterday'}")
        print(f"📊 Google Sheet ID: {config.SPREADSHEET_ID}")
        print(f"🤖 AI Models: Gemini Pro + OpenAI O3 via Zen MCP")
        print("-" * 50)
        
        try:
            # Run comprehensive analysis
            print("\n📈 Running comprehensive analysis...")
            if target_date:
                # Override the target date in workflow analyzer
                self.workflow_analyzer.yesterday = datetime.strptime(target_date, '%Y-%m-%d')
            
            analysis_results = self.workflow_analyzer.run_daily_analysis()
            
            if 'error' in analysis_results:
                print(f"❌ Analysis failed: {analysis_results['error']}")
                return False
            
            # Generate visualizations
            print("\n📊 Generating visualizations...")
            chart_files = self.reporter.generate_daily_charts(analysis_results)
            
            # Generate HTML report
            print("\n📄 Creating comprehensive report...")
            html_report = self.reporter.generate_html_report(analysis_results, chart_files)
            
            # Save JSON results
            results_file = self._save_analysis_results(analysis_results)
            
            # Display summary
            self._display_summary(analysis_results, html_report, results_file)
            
            # Show Zen MCP prompts
            self._display_zen_prompts(analysis_results)
            
            return True
            
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            print("\n🔧 Troubleshooting:")
            print("1. Check Google Sheets API credentials")
            print("2. Verify your Google Sheet ID in config.py")
            print("3. Ensure your sheet has data in the expected format")
            return False
    
    def setup_credentials(self):
        """Setup Google Sheets API credentials"""
        print("🔐 GOOGLE SHEETS API SETUP")
        print("=" * 30)
        setup_credentials_instructions()
        
        # Test connection
        print("\n🧪 Testing connection...")
        try:
            from google_sheets_auth import GoogleSheetsAuth
            auth = GoogleSheetsAuth()
            if auth.test_connection():
                print("✅ Connection successful!")
                return True
            else:
                print("❌ Connection failed. Please check your credentials.")
                return False
        except Exception as e:
            print(f"❌ Setup error: {str(e)}")
            return False
    
    def configure_budgets(self):
        """Interactive budget configuration"""
        print("💰 BUDGET CONFIGURATION")
        print("=" * 25)
        print("Current daily budget limits:")
        
        for category, limit in config.DAILY_BUDGET_LIMITS.items():
            print(f"  {category}: ${limit:.2f}")
        
        print(f"\n📝 To modify budgets, edit: {os.path.join(os.path.dirname(__file__), 'config.py')}")
        print("Update the DAILY_BUDGET_LIMITS dictionary with your preferred amounts.")
    
    def test_zen_integration(self):
        """Test Zen MCP integration"""
        print("🤖 ZEN MCP INTEGRATION TEST")
        print("=" * 28)
        
        # Check if zen server is accessible
        zen_path = "/Users/bradyswanson2/zen-mcp-server"
        if os.path.exists(zen_path):
            print(f"✅ Zen MCP Server found at: {zen_path}")
        else:
            print(f"❌ Zen MCP Server not found at: {zen_path}")
            print("Please ensure Zen MCP is installed and configured.")
            return False
        
        # Test sample analysis
        print("\n🧪 Testing Zen analysis generation...")
        try:
            from zen_analyzer import ZenAnalyzer
            import pandas as pd
            
            # Create sample data
            sample_data = pd.DataFrame({
                'Date': pd.to_datetime(['2025-01-29'] * 3),
                'Description': ['Starbucks Coffee', 'Uber Ride', 'Amazon Purchase'],
                'Amount': [-5.50, -12.00, -45.99],
                'Category': ['Food & Dining', 'Transportation', 'Shopping'],
                'Is_Expense': [True, True, True],
                'Abs_Amount': [5.50, 12.00, 45.99]
            })
            
            analyzer = ZenAnalyzer()
            analyses = analyzer.generate_comprehensive_analysis(sample_data, {'total_spent': 63.49})
            
            print("✅ Zen analysis prompts generated successfully!")
            print("🎯 Ready to use with Claude Code CLI")
            return True
            
        except Exception as e:
            print(f"❌ Zen integration test failed: {str(e)}")
            return False
    
    def _save_analysis_results(self, analysis_results):
        """Save analysis results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"/Users/bradyswanson2/transaction-analyzer/results/analysis_{timestamp}.json"
        
        # Ensure results directory exists
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        return results_file
    
    def _display_summary(self, analysis_results, html_report, results_file):
        """Display analysis summary"""
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 20)
        
        # Key metrics
        daily_summary = analysis_results.get('daily_summary', {})
        basic_summary = daily_summary.get('basic_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        
        print(f"📊 Total Spent: ${basic_summary.get('total_spent', 0):.2f}")
        print(f"🎯 Risk Level: {overspending.get('risk_level', 'Unknown')}")
        print(f"📈 Spending Score: {overspending.get('spending_score', 0)}/100")
        
        # Alerts
        overspending_alerts = len(overspending.get('overspending_alerts', []))
        if overspending_alerts > 0:
            print(f"⚠️ Overspending Alerts: {overspending_alerts}")
        
        # Opportunities
        opportunities = analysis_results.get('opportunity_analysis', {})
        potential_savings = opportunities.get('total_potential_savings', 0)
        if potential_savings > 0:
            print(f"💰 Potential Savings: ${potential_savings:.2f}")
        
        print(f"\n📄 Reports Generated:")
        print(f"  • HTML Report: {html_report}")
        print(f"  • JSON Data: {results_file}")
        
        # Charts
        charts_dir = "/Users/bradyswanson2/transaction-analyzer/reports/charts"
        if os.path.exists(charts_dir):
            chart_count = len([f for f in os.listdir(charts_dir) if f.endswith('.png')])
            print(f"  • Charts: {chart_count} generated in {charts_dir}")
    
    def _display_zen_prompts(self, analysis_results):
        """Display Zen MCP prompts for Claude Code CLI"""
        print("\n🤖 ZEN MCP AI ANALYSIS")
        print("=" * 25)
        print("Ready for AI-powered insights! Use these prompts in Claude Code CLI:")
        print()
        
        # Basic analysis prompt
        date_str = analysis_results['metadata']['target_date']
        print("🎯 QUICK START PROMPT:")
        print("-" * 20)
        print(f"Use zen consensus to analyze my spending patterns from {date_str}. ")
        print("I want to understand where I'm overspending and get actionable advice from both gemini pro and o3.")
        print()
        
        # Specific prompts based on analysis
        daily_summary = analysis_results.get('daily_summary', {})
        overspending = daily_summary.get('overspending_analysis', {})
        
        if overspending.get('overspending_alerts'):
            print("🚨 OVERSPENDING ANALYSIS:")
            print("-" * 25)
            categories = [alert['category'] for alert in overspending['overspending_alerts']]
            print(f"Use zen debug to systematically investigate why I'm overspending on {', '.join(categories)}. ")
            print("Find the root causes and suggest specific behavioral changes.")
            print()
        
        # Opportunities prompt
        opportunities = analysis_results.get('opportunity_analysis', {})
        if opportunities.get('total_potential_savings', 0) > 0:
            savings = opportunities['total_potential_savings']
            print("💡 OPTIMIZATION ANALYSIS:")
            print("-" * 25)
            print(f"Use zen thinkdeep with gemini pro to analyze my ${savings:.2f} potential savings opportunities. ")
            print("Prioritize them by impact and feasibility, then create an implementation plan.")
            print()
        
        print("🔧 AVAILABLE ZEN TOOLS:")
        print("• consensus - Multi-model perspective on spending decisions")
        print("• debug - Systematic investigation of overspending issues") 
        print("• thinkdeep - Extended reasoning about financial habits")
        print("• analyze - Deep analysis of spending patterns")
        print("• planner - Step-by-step financial improvement planning")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Transaction Analyzer with Zen MCP Integration')
    parser.add_argument('--setup', action='store_true', help='Setup Google Sheets API credentials')
    parser.add_argument('--config', action='store_true', help='Configure budgets')
    parser.add_argument('--test-zen', action='store_true', help='Test Zen MCP integration')
    parser.add_argument('--date', type=str, help='Target date for analysis (YYYY-MM-DD)')
    parser.add_argument('--analyze', action='store_true', help='Run daily analysis (default action)')
    
    args = parser.parse_args()
    
    app = TransactionAnalyzerApp()
    
    if args.setup:
        app.setup_credentials()
    elif args.config:
        app.configure_budgets()
    elif args.test_zen:
        app.test_zen_integration()
    else:
        # Default action: run analysis
        success = app.run_daily_analysis(args.date)
        if not success:
            print("\n🔧 QUICK SETUP:")
            print("1. Run: python main.py --setup")
            print("2. Run: python main.py --test-zen")
            print("3. Run: python main.py --analyze")


if __name__ == "__main__":
    main()