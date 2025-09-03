# 🚀 Transaction Analyzer - Setup Guide

Your intelligent transaction analyzer with AI-powered insights is ready! Here's how to get started:

## ✅ System Status
- ✅ All dependencies installed
- ✅ Overspending detection working
- ✅ Zen MCP integration ready
- ✅ Visualizations generating
- ✅ Sample data test successful

## 🔐 Google Sheets API Setup

1. **Get Google Credentials:**
   ```bash
   python3 main.py --setup
   ```
   Follow the detailed instructions to:
   - Create a Google Cloud project
   - Enable Sheets API
   - Download credentials.json

2. **Place credentials file:**
   ```
   /Users/bradyswanson2/transaction-analyzer/credentials.json
   ```

## 📊 Google Sheets Format

Your sheet should have these columns:
- **Date** (YYYY-MM-DD format)
- **Description** (transaction description)
- **Amount** (negative for expenses, positive for income)
- **Category** (Food & Dining, Transportation, Shopping, etc.)

## 🎯 Daily Analysis Workflow

### Method 1: Automated Analysis
```bash
cd /Users/bradyswanson2/transaction-analyzer
python3 main.py
```

### Method 2: Test with Sample Data
```bash
python3 test_sample_data.py
```

## 🤖 AI Analysis Integration

The system generates prompts for Claude Code CLI. After running analysis:

1. Copy the generated Zen prompt
2. Open Claude Code CLI
3. Use consensus analysis with multiple models:
   ```
   Use zen consensus to analyze my spending data...
   ```

## 📈 Generated Outputs

Each run creates:
- **HTML Report:** `/reports/daily_report_YYYY-MM-DD.html`
- **Charts:** `/reports/charts/` (spending breakdown, budget comparison, heatmaps)
- **AI Prompts:** Ready for Claude Code integration

## 🚨 Overspending Detection

Automatically detects:
- Daily budget overruns by category
- Risk level assessment (Low/Medium/High/Critical)
- Spending score (0-100)
- Actionable recommendations

## 🛠 Configuration

Edit `config.py` to customize:
- Daily budgets by category
- Risk thresholds
- Analysis preferences

## 🎉 You're Ready!

Your system is fully operational. Run the analysis and start getting AI-powered insights into your spending patterns!