"""
Streamlit Web Application for Tesla Supercharger Profitability Calculator

Interactive web interface with comprehensive financial modeling.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from calculator_enhanced import (
    EnhancedSuperchargerCalculator,
    InstallationCosts,
    EquipmentCosts,
    LicensingLegalCosts,
    AnnualOperatingCosts,
    RevenueParameters
)
from market_analysis import MarketAnalyzer

# Page configuration
st.set_page_config(
    page_title="Tesla Supercharger Profitability Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E82127;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .warning {
        color: #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">⚡ Tesla Supercharger Profitability Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Comprehensive Financial Analysis for Charging Infrastructure</div>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.title("Configuration")
st.sidebar.markdown("Adjust parameters to model your specific scenario")

# Installation Costs
with st.sidebar.expander("🏗️ Installation Costs", expanded=False):
    site_prep = st.number_input("Site Preparation ($)", value=50000, step=5000, min_value=0)
    electrical_infra = st.number_input("Electrical Infrastructure ($)", value=150000, step=10000, min_value=0)
    concrete = st.number_input("Concrete & Construction ($)", value=40000, step=5000, min_value=0)
    labor = st.number_input("Labor Costs ($)", value=80000, step=5000, min_value=0)
    permitting = st.number_input("Permitting & Inspections ($)", value=25000, step=5000, min_value=0)
    environmental = st.number_input("Environmental Compliance ($)", value=15000, step=5000, min_value=0)
    contingency = st.number_input("Contingency Buffer ($)", value=25000, step=5000, min_value=0)

# Equipment Costs
with st.sidebar.expander("🔌 Equipment Costs", expanded=False):
    num_stalls = st.number_input("Number of Charging Stalls", value=8, min_value=1, max_value=50)
    charger_cost = st.number_input("Charger Unit Cost ($)", value=30000, step=5000, min_value=0)
    transformer = st.number_input("Transformer Cost ($)", value=45000, step=5000, min_value=0)
    switchgear = st.number_input("Switchgear ($)", value=35000, step=5000, min_value=0)
    cabling = st.number_input("Cabling & Materials ($)", value=25000, step=5000, min_value=0)
    canopy = st.number_input("Canopy/Shelter ($)", value=80000, step=10000, min_value=0)
    signage = st.number_input("Signage & Lighting ($)", value=15000, step=5000, min_value=0)
    payment_systems = st.number_input("Payment Systems ($)", value=12000, step=2000, min_value=0)
    monitoring = st.number_input("Monitoring Systems ($)", value=18000, step=2000, min_value=0)

# Licensing & Legal
with st.sidebar.expander("📋 Licensing & Legal", expanded=False):
    business_lic = st.number_input("Business Licenses ($)", value=5000, step=1000, min_value=0)
    env_permits = st.number_input("Environmental Permits ($)", value=8000, step=1000, min_value=0)
    legal_fees = st.number_input("Legal Fees ($)", value=12000, step=2000, min_value=0)
    insurance_setup = st.number_input("Insurance Setup ($)", value=3000, step=500, min_value=0)
    branding = st.number_input("Trademark & Branding ($)", value=5000, step=1000, min_value=0)

# Annual Operating Costs
with st.sidebar.expander("💰 Annual Operating Costs", expanded=False):
    land_lease = st.number_input("Land Lease/Rent ($/year)", value=36000, step=5000, min_value=0)
    property_tax = st.number_input("Property Taxes ($/year)", value=12000, step=2000, min_value=0)
    business_tax = st.number_input("Business Taxes ($/year)", value=8000, step=1000, min_value=0)
    insurance_annual = st.number_input("Insurance Annual ($/year)", value=15000, step=2000, min_value=0)
    maintenance_contract = st.number_input("Maintenance Contract ($/year)", value=20000, step=2000, min_value=0)
    cleaning = st.number_input("Cleaning & Upkeep ($/year)", value=8000, step=1000, min_value=0)
    security = st.number_input("Security/Monitoring ($/year)", value=6000, step=1000, min_value=0)
    network = st.number_input("Network Connectivity ($/year)", value=3600, step=500, min_value=0)
    software_fees = st.number_input("Software/Management Fees ($/year)", value=12000, step=2000, min_value=0)
    utilities = st.number_input("Utilities Non-Charging ($/year)", value=4000, step=500, min_value=0)
    repairs = st.number_input("Repairs Reserve ($/year)", value=10000, step=2000, min_value=0)

# Revenue Parameters
with st.sidebar.expander("📈 Revenue & Pricing", expanded=True):
    st.markdown("**Pricing Tiers ($/kWh)**")
    peak_price = st.number_input("Peak Hours (4pm-9pm)", value=0.42, step=0.01, min_value=0.0)
    standard_price = st.number_input("Standard Hours", value=0.35, step=0.01, min_value=0.0)
    off_peak_price = st.number_input("Off-Peak (midnight-6am)", value=0.28, step=0.01, min_value=0.0)

    st.markdown("**Usage Distribution**")
    peak_percent = st.slider("Peak Usage %", 0, 100, 25) / 100
    standard_percent = st.slider("Standard Usage %", 0, 100, 60) / 100
    off_peak_percent = st.slider("Off-Peak Usage %", 0, 100, 15) / 100

    st.markdown("**Session Characteristics**")
    avg_kwh = st.number_input("Avg kWh per Session", value=50, step=5, min_value=1)
    sessions_per_day = st.number_input("Sessions per Stall per Day", value=6.0, step=0.5, min_value=0.0)
    utilization = st.slider("Utilization Rate %", 0, 100, 70) / 100

    st.markdown("**Additional Revenue**")
    idle_fee = st.number_input("Idle Fee ($/minute)", value=0.50, step=0.10, min_value=0.0)
    idle_minutes = st.number_input("Avg Idle Minutes", value=5, step=1, min_value=0)
    idle_occurrence = st.slider("Idle Fee Occurrence %", 0, 100, 30) / 100

    membership_fee = st.number_input("Monthly Membership ($)", value=9.99, step=1.0, min_value=0.0)
    member_percent = st.slider("Members %", 0, 100, 15) / 100
    member_discount = st.number_input("Member Discount ($/kWh)", value=0.05, step=0.01, min_value=0.0)

# Electricity Costs
with st.sidebar.expander("⚡ Electricity Costs", expanded=False):
    elec_peak = st.number_input("Peak Rate ($/kWh)", value=0.18, step=0.01, min_value=0.0)
    elec_standard = st.number_input("Standard Rate ($/kWh)", value=0.14, step=0.01, min_value=0.0)
    elec_off_peak = st.number_input("Off-Peak Rate ($/kWh)", value=0.10, step=0.01, min_value=0.0)

# Seasonal Variations
with st.sidebar.expander("📅 Seasonal Variations", expanded=False):
    summer_mult = st.slider("Summer Multiplier", 0.5, 2.0, 1.15, 0.05)
    winter_mult = st.slider("Winter Multiplier", 0.5, 2.0, 0.95, 0.05)
    spring_fall_mult = st.slider("Spring/Fall Multiplier", 0.5, 2.0, 1.00, 0.05)

    weekday_mult = st.slider("Weekday Multiplier", 0.5, 2.0, 1.05, 0.05)
    weekend_mult = st.slider("Weekend Multiplier", 0.5, 2.0, 0.95, 0.05)

# Create calculator instance with user inputs
installation = InstallationCosts(
    site_preparation=site_prep,
    electrical_infrastructure=electrical_infra,
    concrete_construction=concrete,
    labor_costs=labor,
    permitting_inspections=permitting,
    environmental_compliance=environmental,
    contingency=contingency
)

equipment = EquipmentCosts(
    num_stalls=num_stalls,
    charger_unit_cost=charger_cost,
    transformer_cost=transformer,
    switchgear_cost=switchgear,
    cabling_materials=cabling,
    canopy_shelter=canopy,
    signage_lighting=signage,
    payment_systems=payment_systems,
    monitoring_systems=monitoring
)

licensing = LicensingLegalCosts(
    business_licenses=business_lic,
    environmental_permits=env_permits,
    legal_fees=legal_fees,
    insurance_setup=insurance_setup,
    trademark_branding=branding
)

operating = AnnualOperatingCosts(
    land_lease_rent=land_lease,
    property_taxes=property_tax,
    business_taxes=business_tax,
    insurance_annual=insurance_annual,
    maintenance_contract=maintenance_contract,
    cleaning_upkeep=cleaning,
    security_monitoring=security,
    network_connectivity=network,
    software_management_fees=software_fees,
    utilities_non_charging=utilities,
    repairs_reserve=repairs
)

revenue = RevenueParameters(
    num_stalls=num_stalls,
    peak_price=peak_price,
    standard_price=standard_price,
    off_peak_price=off_peak_price,
    peak_usage_percent=peak_percent,
    standard_usage_percent=standard_percent,
    off_peak_usage_percent=off_peak_percent,
    avg_kwh_per_session=avg_kwh,
    sessions_per_stall_per_day=sessions_per_day,
    utilization_rate=utilization,
    idle_fee_per_minute=idle_fee,
    avg_idle_minutes_per_session=idle_minutes,
    idle_fee_occurrence_rate=idle_occurrence,
    membership_monthly_fee=membership_fee,
    percent_members=member_percent,
    member_discount_per_kwh=member_discount,
    summer_multiplier=summer_mult,
    winter_multiplier=winter_mult,
    spring_fall_multiplier=spring_fall_mult,
    electricity_rate_peak=elec_peak,
    electricity_rate_standard=elec_standard,
    electricity_rate_off_peak=elec_off_peak,
    weekday_multiplier=weekday_mult,
    weekend_multiplier=weekend_mult
)

calculator = EnhancedSuperchargerCalculator(
    installation=installation,
    equipment=equipment,
    licensing=licensing,
    operating=operating,
    revenue=revenue
)

# Generate report
report = calculator.generate_comprehensive_report()

# Main content area
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "💵 Financial Details",
    "📈 Projections",
    "⚡ Usage Analytics",
    "🗺️ Market Analysis",
    "📄 Export Report"
])

with tab1:
    st.header("Executive Summary")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Initial Investment",
            f"${report['initial_investment']['total']:,.0f}",
            help="Total upfront capital required"
        )

    with col2:
        st.metric(
            "Annual Revenue",
            f"${report['annual_revenue']['total_revenue']:,.0f}",
            help="Total yearly revenue from all sources"
        )

    with col3:
        annual_profit = report['annual_profit']
        profit_color = "normal" if annual_profit > 0 else "inverse"
        st.metric(
            "Annual Profit",
            f"${annual_profit:,.0f}",
            delta=None,
            delta_color=profit_color,
            help="Net profit after all expenses"
        )

    with col4:
        roi = report['roi_metrics']['roi_percentage']
        st.metric(
            "ROI",
            f"{roi:.1f}%",
            help="Annual return on investment"
        )

    st.markdown("---")

    # Payback and projections
    col1, col2, col3 = st.columns(3)

    with col1:
        payback = report['roi_metrics']['payback_period_years']
        if payback == float('inf'):
            st.metric("Payback Period", "Never", help="Years to recover investment")
        else:
            st.metric("Payback Period", f"{payback:.1f} years", help="Years to recover investment")

    with col2:
        year_5 = report['roi_metrics']['year_5_cumulative_profit']
        st.metric("5-Year Profit", f"${year_5:,.0f}", help="Cumulative profit after 5 years")

    with col3:
        year_10 = report['roi_metrics']['year_10_cumulative_profit']
        st.metric("10-Year Profit", f"${year_10:,.0f}", help="Cumulative profit after 10 years")

    # Recommendation
    st.markdown("---")
    st.subheader("Investment Recommendation")

    if annual_profit > 0 and payback < 5:
        st.success("✅ **Excellent Investment Opportunity** - Strong profitability with quick payback")
    elif annual_profit > 0 and payback < 7:
        st.info("✓ **Good Investment Opportunity** - Positive returns with reasonable payback period")
    elif annual_profit > 0:
        st.warning("⚠️ **Marginal Investment** - Profitable but long payback period")
    else:
        st.error("❌ **Not Recommended** - Unprofitable with current parameters")

    # Visual breakdown
    st.markdown("---")
    st.subheader("Cost vs Revenue Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        # Initial investment pie chart
        inv_data = report['initial_investment']
        fig_inv = go.Figure(data=[go.Pie(
            labels=['Installation', 'Equipment', 'Licensing & Legal'],
            values=[inv_data['installation'], inv_data['equipment'], inv_data['licensing_legal']],
            hole=0.4,
            marker_colors=['#E82127', '#393C41', '#5C6BC0']
        )])
        fig_inv.update_layout(
            title_text="Initial Investment Breakdown",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_inv, use_container_width=True)

    with col2:
        # Annual revenue pie chart
        rev_data = report['annual_revenue']
        fig_rev = go.Figure(data=[go.Pie(
            labels=['Charging Revenue', 'Idle Fees', 'Memberships'],
            values=[
                rev_data['charging_revenue'],
                rev_data['idle_fees'],
                rev_data['memberships']
            ],
            hole=0.4,
            marker_colors=['#28a745', '#ffc107', '#17a2b8']
        )])
        fig_rev.update_layout(
            title_text="Annual Revenue Breakdown",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_rev, use_container_width=True)

with tab2:
    st.header("Detailed Financial Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Initial Investment Details")

        st.markdown("**Installation Costs**")
        st.write(f"Site Preparation: ${site_prep:,.0f}")
        st.write(f"Electrical Infrastructure: ${electrical_infra:,.0f}")
        st.write(f"Concrete & Construction: ${concrete:,.0f}")
        st.write(f"Labor: ${labor:,.0f}")
        st.write(f"Permitting: ${permitting:,.0f}")
        st.write(f"Environmental: ${environmental:,.0f}")
        st.write(f"Contingency: ${contingency:,.0f}")
        st.markdown(f"**Total: ${installation.total():,.0f}**")

        st.markdown("**Equipment Costs**")
        st.write(f"Chargers ({num_stalls} × ${charger_cost:,.0f}): ${num_stalls * charger_cost:,.0f}")
        st.write(f"Transformer: ${transformer:,.0f}")
        st.write(f"Switchgear: ${switchgear:,.0f}")
        st.write(f"Cabling: ${cabling:,.0f}")
        st.write(f"Canopy: ${canopy:,.0f}")
        st.write(f"Signage: ${signage:,.0f}")
        st.write(f"Payment Systems: ${payment_systems:,.0f}")
        st.write(f"Monitoring: ${monitoring:,.0f}")
        st.markdown(f"**Total: ${equipment.total():,.0f}**")

        st.markdown("**Licensing & Legal**")
        st.write(f"Business Licenses: ${business_lic:,.0f}")
        st.write(f"Environmental Permits: ${env_permits:,.0f}")
        st.write(f"Legal Fees: ${legal_fees:,.0f}")
        st.write(f"Insurance Setup: ${insurance_setup:,.0f}")
        st.write(f"Branding: ${branding:,.0f}")
        st.markdown(f"**Total: ${licensing.total():,.0f}**")

    with col2:
        st.subheader("Annual Revenue Details")

        charging_detail = report['charging_revenue_detail']
        st.markdown("**Charging Revenue by Tier**")
        st.write(f"Peak Hours: ${charging_detail['peak_revenue']:,.0f} ({charging_detail['peak_kwh']:,.0f} kWh)")
        st.write(f"Standard Hours: ${charging_detail['standard_revenue']:,.0f} ({charging_detail['standard_kwh']:,.0f} kWh)")
        st.write(f"Off-Peak: ${charging_detail['off_peak_revenue']:,.0f} ({charging_detail['off_peak_kwh']:,.0f} kWh)")
        st.markdown(f"**Subtotal: ${charging_detail['total_charging_revenue']:,.0f}**")

        additional = report['additional_revenue']
        st.markdown("**Additional Revenue**")
        st.write(f"Idle Fees: ${additional['idle_fee_revenue']:,.0f}")
        st.write(f"Memberships: ${additional['membership_revenue']:,.0f}")
        st.markdown(f"**Subtotal: ${additional['total_additional_revenue']:,.0f}**")

        st.markdown(f"### Total Annual Revenue: ${report['annual_revenue']['total_revenue']:,.0f}")

        st.markdown("---")
        st.subheader("Annual Cost Details")

        elec_costs = report['electricity_breakdown']
        st.markdown("**Electricity Costs**")
        st.write(f"Peak Rate: ${elec_costs['peak_electricity_cost']:,.0f}")
        st.write(f"Standard Rate: ${elec_costs['standard_electricity_cost']:,.0f}")
        st.write(f"Off-Peak Rate: ${elec_costs['off_peak_electricity_cost']:,.0f}")
        st.markdown(f"**Subtotal: ${elec_costs['total_electricity_cost']:,.0f}**")

        st.markdown("**Fixed Operating Costs**")
        st.write(f"Land Lease: ${land_lease:,.0f}")
        st.write(f"Property Taxes: ${property_tax:,.0f}")
        st.write(f"Business Taxes: ${business_tax:,.0f}")
        st.write(f"Insurance: ${insurance_annual:,.0f}")
        st.write(f"Maintenance: ${maintenance_contract:,.0f}")
        st.write(f"Cleaning: ${cleaning:,.0f}")
        st.write(f"Security: ${security:,.0f}")
        st.write(f"Network: ${network:,.0f}")
        st.write(f"Software: ${software_fees:,.0f}")
        st.write(f"Utilities: ${utilities:,.0f}")
        st.write(f"Repairs: ${repairs:,.0f}")
        st.markdown(f"**Subtotal: ${operating.total_fixed():,.0f}**")

        st.markdown(f"### Total Annual Costs: ${report['annual_costs']['total_annual_costs']:,.0f}")

with tab3:
    st.header("Multi-Year Financial Projections")

    # Calculate year-by-year projections
    years = list(range(0, 11))
    cumulative_profit = []
    annual_profit_value = report['annual_profit']
    initial_inv = report['initial_investment']['total']

    for year in years:
        if year == 0:
            cumulative_profit.append(-initial_inv)
        else:
            cumulative_profit.append(cumulative_profit[-1] + annual_profit_value)

    # Create projection chart
    fig_projection = go.Figure()

    fig_projection.add_trace(go.Scatter(
        x=years,
        y=cumulative_profit,
        mode='lines+markers',
        name='Cumulative Profit',
        line=dict(color='#28a745', width=3),
        marker=dict(size=8)
    ))

    # Add break-even line
    fig_projection.add_hline(
        y=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Break-even",
        annotation_position="right"
    )

    fig_projection.update_layout(
        title="10-Year Cumulative Profit Projection",
        xaxis_title="Year",
        yaxis_title="Cumulative Profit ($)",
        hovermode='x unified',
        height=500
    )

    st.plotly_chart(fig_projection, use_container_width=True)

    # Annual cash flow table
    st.subheader("Year-by-Year Cash Flow")

    cash_flow_data = []
    for year in years:
        if year == 0:
            cash_flow_data.append({
                'Year': year,
                'Investment': f"${initial_inv:,.0f}",
                'Revenue': "$0",
                'Costs': "$0",
                'Annual Profit': f"-${initial_inv:,.0f}",
                'Cumulative Profit': f"-${initial_inv:,.0f}"
            })
        else:
            cash_flow_data.append({
                'Year': year,
                'Investment': "$0",
                'Revenue': f"${report['annual_revenue']['total_revenue']:,.0f}",
                'Costs': f"${report['annual_costs']['total_annual_costs']:,.0f}",
                'Annual Profit': f"${annual_profit_value:,.0f}",
                'Cumulative Profit': f"${cumulative_profit[year]:,.0f}"
            })

    df_cashflow = pd.DataFrame(cash_flow_data)
    st.dataframe(df_cashflow, use_container_width=True, hide_index=True)

    # Sensitivity analysis
    st.markdown("---")
    st.subheader("Sensitivity Analysis")

    st.info("🔍 Adjust parameters in the sidebar to see how they affect profitability")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Most Impactful Factors:**")
        st.write("1. Utilization Rate - Directly affects revenue")
        st.write("2. Charging Price - Primary revenue driver")
        st.write("3. Electricity Costs - Major operating expense")
        st.write("4. Sessions per Day - Usage intensity")
        st.write("5. Number of Stalls - Capacity and costs")

    with col2:
        st.markdown("**Optimization Tips:**")
        st.write("• Maximize utilization through strategic location")
        st.write("• Implement dynamic pricing for peak hours")
        st.write("• Negotiate bulk electricity rates")
        st.write("• Optimize idle fees to improve turnover")
        st.write("• Consider membership programs for loyalty")

with tab4:
    st.header("Usage & Session Analytics")

    sessions_data = report['sessions_breakdown']

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Annual Sessions", f"{sessions_data['total_sessions']:,.0f}")
        st.metric("Weekday Sessions", f"{sessions_data['weekday_sessions']:,.0f}")
        st.metric("Weekend Sessions", f"{sessions_data['weekend_sessions']:,.0f}")

    with col2:
        st.metric("Peak Hour Sessions", f"{sessions_data['peak_sessions']:,.0f}")
        st.metric("Standard Hour Sessions", f"{sessions_data['standard_sessions']:,.0f}")
        st.metric("Off-Peak Sessions", f"{sessions_data['off_peak_sessions']:,.0f}")

    # Session distribution chart
    st.subheader("Session Distribution by Time Period")

    fig_sessions = go.Figure(data=[
        go.Bar(
            x=['Peak Hours', 'Standard Hours', 'Off-Peak Hours'],
            y=[
                sessions_data['peak_sessions'],
                sessions_data['standard_sessions'],
                sessions_data['off_peak_sessions']
            ],
            marker_color=['#E82127', '#393C41', '#5C6BC0'],
            text=[
                f"{sessions_data['peak_sessions']:,.0f}",
                f"{sessions_data['standard_sessions']:,.0f}",
                f"{sessions_data['off_peak_sessions']:,.0f}"
            ],
            textposition='auto'
        )
    ])

    fig_sessions.update_layout(
        title="Annual Sessions by Time Period",
        yaxis_title="Number of Sessions",
        height=400
    )

    st.plotly_chart(fig_sessions, use_container_width=True)

    # Revenue per session
    st.subheader("Revenue Metrics")

    total_sessions = sessions_data['total_sessions']
    total_revenue = report['annual_revenue']['total_revenue']
    revenue_per_session = total_revenue / total_sessions if total_sessions > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Revenue per Session", f"${revenue_per_session:.2f}")

    with col2:
        total_kwh = report['charging_revenue_detail']['total_kwh']
        avg_revenue_per_kwh = total_revenue / total_kwh if total_kwh > 0 else 0
        st.metric("Avg Revenue per kWh", f"${avg_revenue_per_kwh:.3f}")

    with col3:
        daily_sessions = total_sessions / 365
        st.metric("Avg Daily Sessions", f"{daily_sessions:.1f}")

with tab5:
    st.header("US Market Analysis")

    st.markdown("""
    Analyze charger density vs population to identify **high-opportunity markets**
    where Supercharger infrastructure is underserved.
    """)

    # Initialize market analyzer
    analyzer = MarketAnalyzer()
    market_data = analyzer.get_market_data()
    national_stats = analyzer.get_national_stats()

    # National overview
    st.subheader("📊 National Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cities Analyzed", f"{national_stats['cities_analyzed']}")

    with col2:
        st.metric("Total Population", f"{national_stats['total_population']:,.0f}")

    with col3:
        st.metric("Total Chargers", f"{national_stats['total_chargers']}")

    with col4:
        st.metric("Avg Chargers/100k", f"{national_stats['avg_chargers_per_100k']:.2f}")

    st.markdown("---")

    # Heat maps
    st.subheader("🗺️ Interactive US Heat Maps")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Charger Density**")

        # Charger density map
        fig_chargers = go.Figure()

        # Add charger locations as bubbles
        fig_chargers.add_trace(go.Scattergeo(
            lon=market_data['lon'],
            lat=market_data['lat'],
            text=[f"{row['city']}, {row['state']}<br>"
                  f"Chargers: {row['chargers']}<br>"
                  f"Per 100k: {row['chargers_per_100k']:.2f}"
                  for _, row in market_data.iterrows()],
            mode='markers',
            marker=dict(
                size=market_data['chargers'] * 2,
                color=market_data['chargers'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Chargers"),
                line=dict(width=0.5, color='white'),
                sizemode='diameter'
            ),
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))

        fig_chargers.update_layout(
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showlakes=True,
                lakecolor='rgb(230, 245, 255)'
            ),
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig_chargers, use_container_width=True)

    with col2:
        st.markdown("**Population Density**")

        # Population density map
        fig_population = go.Figure()

        fig_population.add_trace(go.Scattergeo(
            lon=market_data['lon'],
            lat=market_data['lat'],
            text=[f"{row['city']}, {row['state']}<br>"
                  f"Population: {row['population']:,}<br>"
                  f"Market Size: {row['market_size_score']:.1f}"
                  for _, row in market_data.iterrows()],
            mode='markers',
            marker=dict(
                size=market_data['market_size_score'] / 2,
                color=market_data['population'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Population"),
                line=dict(width=0.5, color='white'),
                sizemode='diameter'
            ),
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))

        fig_population.update_layout(
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                showlakes=True,
                lakecolor='rgb(230, 245, 255)'
            ),
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.plotly_chart(fig_population, use_container_width=True)

    # Gap Analysis Heat Map
    st.markdown("---")
    st.subheader("🎯 Market Opportunity Heat Map")
    st.markdown("**Red = Underserved (High Opportunity) | Green = Oversaturated**")

    fig_gap = go.Figure()

    # Create gap visualization (negative gap = underserved = opportunity)
    fig_gap.add_trace(go.Scattergeo(
        lon=market_data['lon'],
        lat=market_data['lat'],
        text=[f"{row['city']}, {row['state']}<br>"
              f"Population: {row['population']:,}<br>"
              f"Chargers: {row['chargers']}<br>"
              f"Coverage Gap: {row['coverage_gap']:.2f}<br>"
              f"Opportunity Score: {row['opportunity_score']:.1f}"
              for _, row in market_data.iterrows()],
        mode='markers',
        marker=dict(
            size=market_data['opportunity_score'] * 1.5,
            color=-market_data['coverage_gap'],  # Negative so red = underserved
            colorscale='RdYlGn_r',  # Reversed so red is high opportunity
            showscale=True,
            colorbar=dict(
                title="Opportunity",
                ticktext=['Oversaturated', 'Balanced', 'Underserved'],
                tickvals=[-2, 0, 2]
            ),
            line=dict(width=0.5, color='white'),
            sizemode='diameter',
            cmin=-3,
            cmax=3
        ),
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

    fig_gap.update_layout(
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)'
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig_gap, use_container_width=True)

    # Top Opportunities
    st.markdown("---")
    st.subheader("🏆 Top 10 Market Opportunities")
    st.markdown("Cities with the highest potential for new Supercharger installations")

    opportunities = analyzer.get_top_opportunities(10)

    # Format the dataframe
    opportunities_display = opportunities.copy()
    opportunities_display['Location'] = opportunities_display['city'] + ', ' + opportunities_display['state']
    opportunities_display['Population'] = opportunities_display['population'].apply(lambda x: f"{x:,}")
    opportunities_display['Chargers'] = opportunities_display['chargers'].astype(int)
    opportunities_display['People/Charger'] = opportunities_display['people_per_charger'].apply(lambda x: f"{x:,.0f}")
    opportunities_display['Per 100k Pop'] = opportunities_display['chargers_per_100k'].apply(lambda x: f"{x:.2f}")
    opportunities_display['Opportunity Score'] = opportunities_display['opportunity_score'].apply(lambda x: f"{x:.1f}")

    st.dataframe(
        opportunities_display[['Location', 'Population', 'Chargers', 'People/Charger', 'Per 100k Pop', 'Opportunity Score']],
        use_container_width=True,
        hide_index=True
    )

    # Regional Analysis
    st.markdown("---")
    st.subheader("📍 Regional Breakdown")

    regional = analyzer.get_regional_analysis()

    col1, col2 = st.columns(2)

    with col1:
        # Regional bar chart
        fig_regional = go.Figure()

        fig_regional.add_trace(go.Bar(
            x=regional.index,
            y=regional['chargers_per_100k'],
            marker_color=['#E82127', '#393C41', '#5C6BC0', '#28a745', '#ffc107'],
            text=regional['chargers_per_100k'].apply(lambda x: f"{x:.2f}"),
            textposition='auto'
        ))

        fig_regional.update_layout(
            title="Chargers per 100k People by Region",
            xaxis_title="Region",
            yaxis_title="Chargers per 100k",
            height=400
        )

        st.plotly_chart(fig_regional, use_container_width=True)

    with col2:
        # Regional table
        st.markdown("**Regional Statistics**")

        regional_display = regional.copy()
        regional_display['Population'] = regional_display['population'].apply(lambda x: f"{x:,}")
        regional_display['Cities'] = regional_display['cities'].astype(int)
        regional_display['Chargers'] = regional_display['chargers'].astype(int)
        regional_display['Per 100k'] = regional_display['chargers_per_100k'].apply(lambda x: f"{x:.2f}")
        regional_display['People/Charger'] = regional_display['people_per_charger'].apply(lambda x: f"{x:,.0f}")

        st.dataframe(
            regional_display[['Cities', 'Population', 'Chargers', 'Per 100k', 'People/Charger']],
            use_container_width=True
        )

    # Key Insights
    st.markdown("---")
    st.subheader("💡 Key Insights")

    top_opportunity = opportunities.iloc[0]
    most_saturated = analyzer.get_oversaturated_markets(1).iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"""
        **🎯 Best Opportunity: {top_opportunity['city']}, {top_opportunity['state']}**

        - Population: {top_opportunity['population']:,}
        - Current Chargers: {top_opportunity['chargers']}
        - People per Charger: {top_opportunity['people_per_charger']:,.0f}
        - Opportunity Score: {top_opportunity['opportunity_score']:.1f}

        This market is significantly underserved and represents a high-value opportunity
        for new Supercharger installation.
        """)

    with col2:
        st.info(f"""
        **📊 Most Saturated: {most_saturated['city']}, {most_saturated['state']}**

        - Population: {most_saturated['population']:,}
        - Current Chargers: {most_saturated['chargers']}
        - Chargers per 100k: {most_saturated['chargers_per_100k']:.2f}

        This market has high charger density. Consider other locations unless
        there's specific strategic value.
        """)

    st.markdown("---")
    st.markdown("""
    **How to Use This Analysis:**

    1. **Red bubbles** on the opportunity map indicate underserved markets
    2. **Larger bubbles** indicate higher opportunity scores (population + low coverage)
    3. Focus on cities with high population and low chargers per 100k
    4. Consider regional saturation when planning multi-site deployments
    5. Combine this data with your financial model to find optimal locations
    """)

with tab6:
    st.header("Export Report")

    st.markdown("Download comprehensive financial analysis")

    # Create detailed report text
    report_text = f"""
TESLA SUPERCHARGER PROFITABILITY ANALYSIS
{'=' * 80}

CONFIGURATION
Number of Stalls: {num_stalls}
Utilization Rate: {utilization * 100:.1f}%

INITIAL INVESTMENT
{'─' * 80}
Installation Costs:          ${report['initial_investment']['installation']:>15,.2f}
Equipment Costs:             ${report['initial_investment']['equipment']:>15,.2f}
Licensing & Legal:           ${report['initial_investment']['licensing_legal']:>15,.2f}
TOTAL:                       ${report['initial_investment']['total']:>15,.2f}

ANNUAL REVENUE
{'─' * 80}
Charging Revenue:            ${report['annual_revenue']['charging_revenue']:>15,.2f}
Idle Fees:                   ${report['annual_revenue']['idle_fees']:>15,.2f}
Memberships:                 ${report['annual_revenue']['memberships']:>15,.2f}
TOTAL:                       ${report['annual_revenue']['total_revenue']:>15,.2f}

ANNUAL COSTS
{'─' * 80}
Electricity:                 ${report['annual_costs']['electricity_costs']:>15,.2f}
Fixed Operating Costs:       ${report['annual_costs']['fixed_operating_costs']:>15,.2f}
TOTAL:                       ${report['annual_costs']['total_annual_costs']:>15,.2f}

PROFITABILITY METRICS
{'─' * 80}
Annual Net Profit:           ${report['annual_profit']:>15,.2f}
ROI:                         {report['roi_metrics']['roi_percentage']:>15.2f}%
Payback Period:              {report['roi_metrics']['payback_period_years']:>15.2f} years
5-Year Cumulative:           ${report['roi_metrics']['year_5_cumulative_profit']:>15,.2f}
10-Year Cumulative:          ${report['roi_metrics']['year_10_cumulative_profit']:>15,.2f}

USAGE STATISTICS
{'─' * 80}
Total Annual Sessions:       {sessions_data['total_sessions']:>15,.0f}
Peak Sessions:               {sessions_data['peak_sessions']:>15,.0f}
Standard Sessions:           {sessions_data['standard_sessions']:>15,.0f}
Off-Peak Sessions:           {sessions_data['off_peak_sessions']:>15,.0f}

{'=' * 80}
Generated by Tesla Supercharger Profitability Calculator
"""

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download Text Report",
            data=report_text,
            file_name="supercharger_analysis.txt",
            mime="text/plain"
        )

    with col2:
        # Create CSV data
        csv_data = pd.DataFrame([{
            'Initial Investment': report['initial_investment']['total'],
            'Annual Revenue': report['annual_revenue']['total_revenue'],
            'Annual Costs': report['annual_costs']['total_annual_costs'],
            'Annual Profit': report['annual_profit'],
            'ROI %': report['roi_metrics']['roi_percentage'],
            'Payback Years': report['roi_metrics']['payback_period_years'],
            '5-Year Profit': report['roi_metrics']['year_5_cumulative_profit'],
            '10-Year Profit': report['roi_metrics']['year_10_cumulative_profit']
        }])

        st.download_button(
            label="📊 Download CSV Data",
            data=csv_data.to_csv(index=False),
            file_name="supercharger_data.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.subheader("Report Preview")
    st.text(report_text)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Tesla Supercharger Profitability Calculator | "
    "Built with Streamlit | "
    "© 2024"
    "</div>",
    unsafe_allow_html=True
)
