
# Create comprehensive README.md
readme_content = '''# AI Datacenter Vancouver - Interactive Investor Dashboard

An interactive Streamlit-based investor pitch dashboard for Series B fundraising. This dashboard replaces traditional slide decks with dynamic, explorable visualizations and calculations.

## 🎯 Overview

This dashboard presents a comprehensive investment opportunity for AI Datacenter Vancouver's Series B funding round. It includes:

- **Historical performance** (2015-2024) with 32.2% revenue CAGR
- **Financial projections** through IPO (2030)
- **ROI analysis** comparing all funding rounds
- **Interactive calculator** for custom investment scenarios
- **Detailed company metrics** and operational data

## 📊 Features

### Multi-Page Dashboard

1. **Home (app.py)** - Executive summary and key highlights
2. **Overview** - Investment thesis and comparison analysis
3. **ROI Analysis** - Deep dive into investor returns by funding round
4. **Financial Projections** - Revenue, profitability, and growth forecasts
5. **Investment Scenarios** - Interactive calculator with sliders for custom modeling
6. **Company Details** - Operational metrics and business fundamentals

### Interactive Elements

- **Funding round selector buttons** (Seed, Series A, Series B, Series C)
- **Investment amount slider** ($500K - $20M)
- **Exit scenario toggles** (Conservative, Base, Optimistic)
- **Responsive charts** that update based on user selections
- **Sensitivity analysis** showing returns across valuation ranges

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-datacenter-investor-dashboard.git
cd ai-datacenter-investor-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Run the Streamlit app
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository, branch, and `app.py` as the main file
6. Click "Deploy"

Your dashboard will be live at `https://[your-app-name].streamlit.app`

## 📁 Project Structure

```
streamlit_investor_dashboard/
├── app.py                          # Main landing page
├── pages/                          # Multi-page app pages
│   ├── 1_📊_Overview.py
│   ├── 2_💰_ROI_Analysis.py
│   ├── 3_📈_Financial_Projections.py
│   ├── 4_🎯_Investment_Scenarios.py
│   └── 5_📑_Company_Details.py
├── data/                           # All CSV and JSON data files
│   ├── financial_projections_2015_2030.csv
│   ├── investor_roi_summary.csv
│   ├── funding_rounds_overview.csv
│   ├── operational_metrics.csv
│   └── ... (12 total data files)
├── utils/                          # Helper functions
│   ├── calculations.py            # ROI and financial calculations
│   └── visualizations.py          # Plotly chart functions
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 💡 Key Investment Highlights

### Series B Opportunity (2026)

- **Investment:** $8M at $33M post-money valuation
- **Projected MOIC:** 4.85x (at IPO exit)
- **Projected IRR:** 48.4%
- **Holding Period:** 4 years to IPO (2030)
- **Early Exit Option:** 2.42x in 2 years (Series C exit)

### Why Invest Now?

1. **Superior Returns:** 2.85x higher MOIC than Series C
2. **Proven Track Record:** 10 years of 32%+ revenue growth
3. **Strong Unit Economics:** 23.8% net margins in 2024
4. **Market Tailwinds:** Accelerating AI compute demand
5. **Clear Exit Path:** IPO planned for 2030 at $240M valuation

## 🔧 Customization

### Updating Financial Data

Replace CSV files in the `/data` directory with your own financial data. Ensure column names match the expected format:

- `financial_projections_2015_2030.csv`: Year, Revenue, Net_Income, Company_Valuation, etc.
- `investor_roi_summary.csv`: Round, Investment_Amount, MOIC, IRR_%, etc.

### Modifying Calculations

Edit `/utils/calculations.py` to adjust:
- ROI calculation methodology
- Dilution assumptions
- Exit valuation scenarios

### Styling

Modify `.streamlit/config.toml` to change:
- Color scheme (primaryColor, backgroundColor)
- Font family
- Layout settings

## 📈 Data Sources

All financial data is synthetic and generated for demonstration purposes. The data represents:

- 10 years of historical performance (2015-2024)
- 6 years of conservative projections (2025-2030)
- 5 funding rounds (Seed, Series A, B, C, IPO)
- Complete financial statements (Income, Balance Sheet, Cash Flow)
- Operational metrics (servers, GPUs, customers, employees)

## 🛠️ Technology Stack

- **Streamlit** 1.28.0 - Dashboard framework
- **Plotly** 5.17.0 - Interactive visualizations
- **Pandas** 2.1.0 - Data manipulation
- **NumPy** 1.24.3 - Numerical calculations

## 📝 License

Confidential and proprietary. For authorized investors only.

## 🤝 Support

For questions or issues:
- **Technical:** Create a GitHub issue
- **Investor Relations:** investors@aidcvancouver.com
- **General Inquiries:** info@aidcvancouver.com

---

**Disclaimer:** This dashboard contains forward-looking statements subject to risks and uncertainties. 
Past performance does not guarantee future results. See PPM for complete disclaimers.

© 2025 AI Datacenter Vancouver. All rights reserved.
'''

with open(f'{base_dir}/README.md', 'w') as f:
    f.write(readme_content)

print("✓ Created README.md")
