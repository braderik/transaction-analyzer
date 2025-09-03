# Transaction Analyzer with Zen MCP Integration

A comprehensive financial analysis system that uses **Gemini Pro** and **OpenAI O3** through **Zen MCP** to analyze your Google Sheets transaction data and identify overspending patterns.

## 🎯 Features

### Core Analysis Areas (Implemented)
1. **Trend & Variance Analysis** - Track spending changes across categories
2. **Predictive Spend Forecasting** - Project end-of-month spending and budget overruns
3. **Category & Vendor Deep Dive** - Identify top vendors and recurring patterns
4. **Comparative Benchmarks** - Compare your spending vs. averages
5. **Opportunity Analysis** - Find potential savings and optimization opportunities
6. **Budget Sensitivity Analysis** - What-if scenarios for spending reduction
7. **Alerting & Habit Analysis** - Real-time overspending alerts and pattern detection
8. **Transaction Classification** - Data hygiene and categorization improvements
9. **Cash Flow Health Check** - Income vs. expenses analysis
10. **AI-Powered Insights** - Multi-model analysis via Zen MCP

### AI Integration
- **Gemini Pro** - Deep analysis, architecture decisions, extended thinking
- **OpenAI O3** - Logical debugging, reasoning, problem-solving
- **Zen MCP Tools** - consensus, debug, analyze, thinkdeep, planner

## 🚀 Quick Start

### 1. Installation
```bash
cd /Users/bradyswanson2/transaction-analyzer
pip install -r requirements.txt
```

### 2. Setup Google Sheets API
```bash
python main.py --setup
```
Follow the instructions to:
- Create Google Cloud Project
- Enable Google Sheets API
- Download credentials.json
- Authenticate your account

### 3. Configure Your Sheet
Update `config.py` with your Google Sheet ID:
```python
SPREADSHEET_ID = '1L2NAfkWlLMcGKXqABI2NADn4hXhIwLEUEqLZ_DtlpNU'  # Your sheet
```

Your sheet should have columns:
- **Date** (A): YYYY-MM-DD format
- **Description** (B): Transaction description  
- **Amount** (C): Transaction amount (negative for expenses)
- **Category** (D): Optional category
- **Account** (E): Optional account name
- **Notes** (F): Optional notes

### 4. Configure Budgets
```bash
python main.py --config
```
Edit `config.py` to set your daily budget limits:
```python
DAILY_BUDGET_LIMITS = {
    'Food & Dining': 50.0,
    'Transportation': 30.0,
    'Shopping': 40.0,
    'Entertainment': 25.0,
    # ... customize for your needs
}
```

### 5. Test Zen MCP Integration
```bash
python main.py --test-zen
```
Ensures Zen MCP Server is properly configured.

### 6. Run Daily Analysis
```bash
# Analyze yesterday's transactions
python main.py

# Analyze specific date
python main.py --date 2025-01-29
```

## 📊 Analysis Output

### Generated Reports
1. **HTML Report** - Comprehensive visual report with charts
2. **JSON Data** - Raw analysis results for further processing
3. **Charts** - Category pie charts, budget comparisons, trend analysis
4. **Zen MCP Prompts** - Ready-to-use AI analysis prompts

### Key Metrics
- **Spending Score** (0-100) - Overall spending health
- **Risk Level** - Good/Low Risk/Medium Risk/High Risk
- **Category Breakdown** - Spending by category vs. budget
- **Overspending Alerts** - Critical/High/Medium/Low severity
- **Potential Savings** - Identified optimization opportunities

## 🤖 AI-Powered Analysis

After running the analysis, use these prompts in **Claude Code CLI**:

### Quick Start
```
Use zen consensus to analyze my spending patterns from 2025-01-29. 
I want to understand where I'm overspending and get actionable advice from both gemini pro and o3.
```

### Overspending Investigation
```
Use zen debug to systematically investigate why I'm overspending on Food & Dining. 
Find the root causes and suggest specific behavioral changes.
```

### Optimization Planning
```
Use zen thinkdeep with gemini pro to analyze my $47.50 potential savings opportunities. 
Prioritize them by impact and feasibility, then create an implementation plan.
```

### Available Zen Tools
- **consensus** - Multi-model perspective on spending decisions
- **debug** - Systematic investigation of overspending issues
- **thinkdeep** - Extended reasoning about financial habits
- **analyze** - Deep analysis of spending patterns  
- **planner** - Step-by-step financial improvement planning

## 📁 Project Structure

```
transaction-analyzer/
├── main.py                    # Main application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── google_sheets_auth.py      # Google Sheets API authentication
├── transaction_retriever.py   # Data retrieval from Google Sheets
├── zen_analyzer.py           # Zen MCP integration for AI analysis
├── overspending_analyzer.py  # Advanced overspending detection
├── daily_workflow.py         # Comprehensive daily analysis workflow
├── visualization_reporter.py # Charts and HTML report generation
├── reports/                   # Generated reports and charts
│   ├── charts/               # PNG chart files
│   └── daily_report_*.html   # HTML reports
└── results/                  # JSON analysis results
    └── analysis_*.json       # Raw analysis data
```

## ⚙️ Configuration

### Budget Limits (config.py)
```python
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
```

### Analysis Thresholds
```python
OVERSPENDING_THRESHOLD = 1.2  # 20% over budget = overspending
WARNING_THRESHOLD = 0.8       # 80% of budget = warning
```

### Zen MCP Models
```python
ZEN_MODELS = {
    'primary_analyst': 'gemini-pro',  # Deep analysis
    'secondary_analyst': 'o3',        # Logic and patterns  
    'quick_review': 'flash'           # Quick insights
}
```

## 🔧 Troubleshooting

### Common Issues

**Google Sheets Connection Failed**
```bash
python main.py --setup
```
- Verify credentials.json is in the project directory
- Check Google Sheets API is enabled
- Ensure sheet ID is correct in config.py

**No Transaction Data Found**
- Check date format in sheet (YYYY-MM-DD)
- Verify amount column has numeric values
- Ensure sheet name matches RANGE_NAME in config.py

**Zen MCP Not Working**
```bash
python main.py --test-zen
```
- Verify Zen MCP Server is installed at `/Users/bradyswanson2/zen-mcp-server`
- Check Claude Code CLI is configured with Zen MCP
- Test basic Zen commands in Claude Code CLI

### Debug Mode
Set environment variable for detailed logging:
```bash
export LOG_LEVEL=DEBUG
python main.py
```

## 📈 Advanced Usage

### Batch Analysis
Analyze multiple dates:
```bash
for date in 2025-01-27 2025-01-28 2025-01-29; do
    python main.py --date $date
done
```

### Custom Categories
Edit the `EXPENSE_CATEGORIES` in `config.py` to match your spending patterns:
```python
EXPENSE_CATEGORIES = {
    'Food & Dining': ['restaurant', 'starbucks', 'doordash', 'grocery'],
    'Transportation': ['uber', 'lyft', 'gas', 'parking'],
    # ... add your own keywords
}
```

### Automation
Set up daily cron job:
```bash
# Run daily at 9 AM
0 9 * * * cd /Users/bradyswanson2/transaction-analyzer && python main.py
```

## 🎯 Key Benefits

1. **Automated Analysis** - Daily spending insights without manual work
2. **AI-Powered Insights** - Leverage Gemini Pro + OpenAI O3 for deep analysis
3. **Visual Reports** - Professional charts and HTML reports
4. **Actionable Recommendations** - Specific steps to reduce overspending
5. **Trend Detection** - Identify patterns before they become problems
6. **Budget Optimization** - Find savings opportunities automatically

## 🔮 Future Enhancements

- Email/Slack automated reporting
- Mobile app integration
- Machine learning spending predictions
- Integration with bank APIs
- Custom dashboard web interface
- Multi-currency support

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review your Google Sheets format and permissions
3. Test Zen MCP integration separately
4. Verify all configuration settings in `config.py`

---

**Ready to optimize your spending with AI-powered insights!** 🚀💰