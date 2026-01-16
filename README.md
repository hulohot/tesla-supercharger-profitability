# Tesla Supercharger Profitability Calculator

Comprehensive financial analysis tool for determining the profitability of white-labeling Tesla Supercharger installations.

## 🌟 Features

### Interactive Web Application
- **Beautiful Web UI** built with Streamlit for easy, interactive analysis
- **Comprehensive Cost Categories**: Installation, Equipment, Licensing, Operating Costs
- **Granular Revenue Modeling**: Peak/off-peak pricing, memberships, idle fees
- **Visual Analytics**: Interactive charts and graphs
- **Multi-Year Projections**: 10-year financial forecasts
- **Sensitivity Analysis**: Understand key profitability drivers
- **Export Reports**: Download detailed analysis as text or CSV

### Detailed Financial Modeling
- **Installation Costs**: Site prep, electrical infrastructure, construction, labor, permits
- **Equipment Breakdown**: Chargers, transformers, switchgear, canopy, signage
- **Licensing & Legal**: Business licenses, permits, legal fees, insurance
- **Operating Expenses**: Rent, taxes, insurance, maintenance, utilities, network fees
- **Revenue Streams**: Charging fees (peak/standard/off-peak), idle fees, memberships
- **Usage Patterns**: Weekday/weekend variations, seasonal adjustments

## 🚀 Quick Start

### Web Application (Recommended)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Launch the web app:**
```bash
streamlit run app.py
```

3. **Open your browser** to the URL shown (typically http://localhost:8501)

### 📱 Access from Your Phone

Want to use this calculator from your phone anywhere? Deploy it to the cloud for free!

**See the [DEPLOYMENT.md](DEPLOYMENT.md) guide** for step-by-step instructions on:
- Deploying to Streamlit Community Cloud (FREE - 5 minutes)
- Accessing from your phone via web browser
- Adding to your phone's home screen for app-like experience
- Other hosting options (Railway, Render, etc.)

**Quick Deploy**: Go to [share.streamlit.io](https://share.streamlit.io), connect this GitHub repo, and deploy `app.py` - done! 🚀

### Command-Line Interface

#### Basic Calculator
```bash
python3 calculator.py
```

#### Enhanced Calculator with Detailed Modeling
```bash
python3 calculator_enhanced.py
```

## 📊 What's Included

### Three Tools for Different Needs

1. **`app.py`** - Interactive Web Application
   - Best for: Interactive analysis, presentations, exploring scenarios
   - Features: Full GUI, charts, exports, real-time updates

2. **`calculator_enhanced.py`** - Comprehensive Python Calculator
   - Best for: Detailed analysis, custom integrations
   - Features: Granular cost/revenue categories, seasonal modeling

3. **`calculator.py`** - Simple Command-Line Calculator
   - Best for: Quick estimates, scripting
   - Features: Fast, minimal dependencies

## 💰 Cost Categories

### Initial Investment

**Installation Costs** (~$385,000)
- Site preparation and grading
- Electrical infrastructure and utility connections
- Concrete construction
- Labor costs
- Permitting and inspections
- Environmental compliance
- Contingency buffer

**Equipment Costs** (~$437,000 for 8 stalls)
- Charging units ($30k each)
- High-voltage transformer
- Electrical switchgear
- Cabling and materials
- Weather canopy/shelter
- Signage and lighting
- Payment systems
- Monitoring equipment

**Licensing & Legal** (~$33,000)
- Business licenses
- Environmental permits
- Legal fees
- Insurance setup
- Trademark and branding

**Total Initial Investment**: ~$855,000 for 8 stalls

### Annual Operating Costs (~$134,600/year)

**Fixed Costs**:
- Land lease/rent
- Property taxes
- Business taxes
- Insurance
- Maintenance contracts
- Cleaning and upkeep
- Security/monitoring
- Network connectivity
- Software/management fees
- Utilities (non-charging)
- Repairs reserve

**Variable Costs**:
- Electricity (varies by usage)

## 📈 Revenue Modeling

### Pricing Tiers
- **Peak Hours** (4pm-9pm weekdays): Higher pricing for high-demand periods
- **Standard Hours**: Normal pricing for regular demand
- **Off-Peak** (midnight-6am): Lower pricing to encourage off-peak usage

### Additional Revenue
- **Idle Fees**: Charges after charging session completes (turnover incentive)
- **Membership Programs**: Monthly subscriptions with discounted rates
- **Seasonal Adjustments**: Account for summer/winter usage patterns
- **Weekday/Weekend Variations**: Different usage patterns by day of week

## 🎯 Example Scenarios

### Default Configuration (8 Stalls)
- Initial Investment: $855,000
- Annual Revenue: ~$230,000
- Annual Costs: ~$134,600
- Annual Profit: ~$95,400
- ROI: 11.2%
- Payback: ~9 years

### High-Traffic Location (12 Stalls, 85% Utilization)
```bash
streamlit run app.py
# Then adjust: Stalls=12, Utilization=85%, Sessions/day=8
```

### Budget Installation (4 Stalls)
```bash
streamlit run app.py
# Then adjust: Stalls=4, Installation=$50k, Permitting=$10k
```

### Premium Location with High Pricing
```bash
streamlit run app.py
# Then adjust: Peak=$0.45, Standard=$0.38, Off-peak=$0.30
```

## 📱 Web UI Guide

### Navigation Tabs

1. **Overview** - Executive summary with key metrics and recommendations
2. **Financial Details** - Complete breakdown of costs and revenues
3. **Projections** - 10-year financial forecasts and sensitivity analysis
4. **Usage Analytics** - Session statistics and usage patterns
5. **Export Report** - Download comprehensive reports

### Interactive Features

- **Sidebar Controls**: Adjust all parameters in real-time
- **Collapsible Sections**: Organized by category for easy navigation
- **Live Updates**: See results change instantly as you adjust inputs
- **Visual Charts**: Pie charts, bar charts, and line graphs
- **Export Options**: Download text reports or CSV data

## 🔧 Advanced Usage

### Python Library Integration

```python
from calculator_enhanced import (
    EnhancedSuperchargerCalculator,
    InstallationCosts,
    EquipmentCosts,
    RevenueParameters
)

# Create custom configuration
installation = InstallationCosts(
    site_preparation=60000,
    electrical_infrastructure=180000,
    # ... other parameters
)

equipment = EquipmentCosts(
    num_stalls=12,
    charger_unit_cost=32000,
    # ... other parameters
)

revenue = RevenueParameters(
    num_stalls=12,
    peak_price=0.45,
    standard_price=0.37,
    utilization_rate=0.85
)

# Calculate profitability
calc = EnhancedSuperchargerCalculator(
    installation=installation,
    equipment=equipment,
    revenue=revenue
)

report = calc.generate_comprehensive_report()

# Access specific metrics
print(f"ROI: {report['roi_metrics']['roi_percentage']:.2f}%")
print(f"Payback: {report['roi_metrics']['payback_period_years']:.2f} years")
print(f"10-Year Profit: ${report['roi_metrics']['year_10_cumulative_profit']:,.0f}")
```

## 📊 Understanding the Metrics

- **Initial Investment**: Total upfront capital required
- **Annual Revenue**: Yearly income from all sources (charging, fees, memberships)
- **Annual Operating Costs**: All yearly expenses including electricity and fixed costs
- **Annual Net Profit**: Revenue minus all costs
- **ROI (Return on Investment)**: Annual profit as a percentage of initial investment
- **Payback Period**: Years needed to recover initial investment from profits
- **Cumulative Profit**: Total profit after recovering initial investment

## 🎓 Tips for Accurate Modeling

1. **Research Local Costs**: Adjust installation and operating costs for your region
2. **Validate Electricity Rates**: Use actual utility rates including demand charges
3. **Study Traffic Patterns**: Research typical EV charging behavior in your area
4. **Consider Competition**: Adjust pricing based on local market conditions
5. **Account for Growth**: Consider EV adoption trends in your projections
6. **Include All Costs**: Don't forget insurance, permits, legal fees, etc.
7. **Plan for Maintenance**: Set aside adequate reserves for repairs

## 🛠️ Requirements

- Python 3.6 or higher
- For web UI: `streamlit`, `pandas`, `plotly` (see requirements.txt)
- For CLI: No additional dependencies required

## 📄 Files

- `app.py` - Streamlit web application
- `calculator_enhanced.py` - Enhanced calculator with detailed modeling
- `calculator.py` - Simple command-line calculator
- `requirements.txt` - Python dependencies

## 🤝 Contributing

Contributions welcome! This calculator is designed to help make informed decisions about EV charging infrastructure investments.

## 📜 License

See LICENSE file for details.

## ⚠️ Disclaimer

This calculator provides estimates for planning purposes only. Actual costs and revenues will vary based on location, market conditions, regulations, and many other factors. Always conduct thorough due diligence and consult with financial, legal, and technical professionals before making investment decisions.
