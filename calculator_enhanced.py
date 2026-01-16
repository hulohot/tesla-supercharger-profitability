#!/usr/bin/env python3
"""
Enhanced Tesla Supercharger Profitability Calculator

Comprehensive financial modeling for Supercharger installations with detailed
cost breakdown and granular revenue projections.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import json


@dataclass
class InstallationCosts:
    """Detailed breakdown of installation costs."""
    site_preparation: float = 50000  # Grading, drainage, etc.
    electrical_infrastructure: float = 150000  # Utility connection, transformers
    concrete_construction: float = 40000  # Pads, curbs, sidewalks
    labor_costs: float = 80000  # Installation labor
    permitting_inspections: float = 25000  # All permits and inspections
    environmental_compliance: float = 15000  # Environmental assessments
    contingency: float = 25000  # 10% contingency buffer

    def total(self) -> float:
        return (
            self.site_preparation +
            self.electrical_infrastructure +
            self.concrete_construction +
            self.labor_costs +
            self.permitting_inspections +
            self.environmental_compliance +
            self.contingency
        )


@dataclass
class EquipmentCosts:
    """Detailed breakdown of equipment costs."""
    num_stalls: int = 8
    charger_unit_cost: float = 30000  # Per charging unit
    transformer_cost: float = 45000  # High-voltage transformer
    switchgear_cost: float = 35000  # Electrical switchgear
    cabling_materials: float = 25000  # All electrical cabling
    canopy_shelter: float = 80000  # Weather protection (optional)
    signage_lighting: float = 15000  # Wayfinding and illumination
    payment_systems: float = 12000  # Payment terminals/software
    monitoring_systems: float = 18000  # Remote monitoring equipment

    def total(self) -> float:
        return (
            (self.charger_unit_cost * self.num_stalls) +
            self.transformer_cost +
            self.switchgear_cost +
            self.cabling_materials +
            self.canopy_shelter +
            self.signage_lighting +
            self.payment_systems +
            self.monitoring_systems
        )


@dataclass
class LicensingLegalCosts:
    """Licensing and legal setup costs."""
    business_licenses: float = 5000
    environmental_permits: float = 8000
    legal_fees: float = 12000
    insurance_setup: float = 3000
    trademark_branding: float = 5000

    def total(self) -> float:
        return (
            self.business_licenses +
            self.environmental_permits +
            self.legal_fees +
            self.insurance_setup +
            self.trademark_branding
        )


@dataclass
class AnnualOperatingCosts:
    """Annual ongoing operating expenses."""
    land_lease_rent: float = 36000  # Monthly rent/lease
    property_taxes: float = 12000
    business_taxes: float = 8000
    insurance_annual: float = 15000  # Liability, property insurance
    maintenance_contract: float = 20000  # Service agreements
    cleaning_upkeep: float = 8000
    security_monitoring: float = 6000
    network_connectivity: float = 3600  # Internet, cellular
    software_management_fees: float = 12000  # Management platform
    utilities_non_charging: float = 4000  # Lighting, etc.
    repairs_reserve: float = 10000  # Unexpected repairs

    def total_fixed(self) -> float:
        """Fixed costs (not including electricity)."""
        return (
            self.land_lease_rent +
            self.property_taxes +
            self.business_taxes +
            self.insurance_annual +
            self.maintenance_contract +
            self.cleaning_upkeep +
            self.security_monitoring +
            self.network_connectivity +
            self.software_management_fees +
            self.utilities_non_charging +
            self.repairs_reserve
        )


@dataclass
class RevenueParameters:
    """Granular revenue modeling parameters."""
    num_stalls: int = 8

    # Pricing tiers (per kWh)
    peak_price: float = 0.42  # High-demand hours (4pm-9pm weekdays)
    standard_price: float = 0.35  # Normal hours
    off_peak_price: float = 0.28  # Low-demand (midnight-6am)

    # Usage patterns (percentage of total sessions)
    peak_usage_percent: float = 0.25
    standard_usage_percent: float = 0.60
    off_peak_usage_percent: float = 0.15

    # Session characteristics
    avg_kwh_per_session: float = 50
    sessions_per_stall_per_day: float = 6
    utilization_rate: float = 0.70

    # Additional revenue streams
    idle_fee_per_minute: float = 0.50  # Fee after charging complete
    avg_idle_minutes_per_session: float = 5
    idle_fee_occurrence_rate: float = 0.30  # 30% of sessions incur idle fees

    membership_monthly_fee: float = 9.99
    percent_members: float = 0.15  # 15% of regular users are members
    member_discount_per_kwh: float = 0.05  # Member discount

    # Seasonal variation multipliers
    summer_multiplier: float = 1.15  # 15% higher in summer
    winter_multiplier: float = 0.95  # 5% lower in winter
    spring_fall_multiplier: float = 1.00

    # Electricity costs
    electricity_rate_peak: float = 0.18
    electricity_rate_standard: float = 0.14
    electricity_rate_off_peak: float = 0.10

    # Weekday vs Weekend
    weekday_multiplier: float = 1.05
    weekend_multiplier: float = 0.95


class EnhancedSuperchargerCalculator:
    """Comprehensive profitability calculator with detailed modeling."""

    def __init__(
        self,
        installation: InstallationCosts = None,
        equipment: EquipmentCosts = None,
        licensing: LicensingLegalCosts = None,
        operating: AnnualOperatingCosts = None,
        revenue: RevenueParameters = None
    ):
        self.installation = installation or InstallationCosts()
        self.equipment = equipment or EquipmentCosts()
        self.licensing = licensing or LicensingLegalCosts()
        self.operating = operating or AnnualOperatingCosts()
        self.revenue = revenue or RevenueParameters()

    def calculate_total_initial_investment(self) -> Dict[str, float]:
        """Calculate total upfront investment with breakdown."""
        return {
            'installation': self.installation.total(),
            'equipment': self.equipment.total(),
            'licensing_legal': self.licensing.total(),
            'total': (
                self.installation.total() +
                self.equipment.total() +
                self.licensing.total()
            )
        }

    def calculate_annual_sessions(self) -> Dict[str, float]:
        """Calculate annual charging sessions breakdown."""
        total_sessions = (
            self.revenue.num_stalls *
            self.revenue.sessions_per_stall_per_day *
            365 *
            self.revenue.utilization_rate
        )

        # Account for weekday/weekend variation
        weekday_sessions = total_sessions * (5/7) * self.revenue.weekday_multiplier
        weekend_sessions = total_sessions * (2/7) * self.revenue.weekend_multiplier
        adjusted_total = weekday_sessions + weekend_sessions

        return {
            'weekday_sessions': weekday_sessions,
            'weekend_sessions': weekend_sessions,
            'total_sessions': adjusted_total,
            'peak_sessions': adjusted_total * self.revenue.peak_usage_percent,
            'standard_sessions': adjusted_total * self.revenue.standard_usage_percent,
            'off_peak_sessions': adjusted_total * self.revenue.off_peak_usage_percent
        }

    def calculate_charging_revenue(self) -> Dict[str, float]:
        """Calculate revenue from charging with detailed breakdown."""
        sessions = self.calculate_annual_sessions()

        # Calculate kWh delivered by tier
        peak_kwh = sessions['peak_sessions'] * self.revenue.avg_kwh_per_session
        standard_kwh = sessions['standard_sessions'] * self.revenue.avg_kwh_per_session
        off_peak_kwh = sessions['off_peak_sessions'] * self.revenue.avg_kwh_per_session

        # Calculate revenue by tier (accounting for member discount)
        member_adjustment = 1 - (self.revenue.percent_members *
                                 (self.revenue.member_discount_per_kwh / self.revenue.standard_price))

        peak_revenue = peak_kwh * self.revenue.peak_price * member_adjustment
        standard_revenue = standard_kwh * self.revenue.standard_price * member_adjustment
        off_peak_revenue = off_peak_kwh * self.revenue.off_peak_price * member_adjustment

        # Apply seasonal variation (simplified average)
        seasonal_avg = (
            self.revenue.summer_multiplier * 0.25 +
            self.revenue.winter_multiplier * 0.25 +
            self.revenue.spring_fall_multiplier * 0.50
        )

        return {
            'peak_revenue': peak_revenue * seasonal_avg,
            'standard_revenue': standard_revenue * seasonal_avg,
            'off_peak_revenue': off_peak_revenue * seasonal_avg,
            'total_charging_revenue': (peak_revenue + standard_revenue + off_peak_revenue) * seasonal_avg,
            'peak_kwh': peak_kwh,
            'standard_kwh': standard_kwh,
            'off_peak_kwh': off_peak_kwh,
            'total_kwh': peak_kwh + standard_kwh + off_peak_kwh
        }

    def calculate_additional_revenue(self) -> Dict[str, float]:
        """Calculate revenue from idle fees and memberships."""
        sessions = self.calculate_annual_sessions()

        # Idle fee revenue
        idle_sessions = sessions['total_sessions'] * self.revenue.idle_fee_occurrence_rate
        idle_revenue = (
            idle_sessions *
            self.revenue.avg_idle_minutes_per_session *
            self.revenue.idle_fee_per_minute
        )

        # Membership revenue
        # Estimate unique customers (sessions / avg sessions per customer per month)
        avg_sessions_per_customer_monthly = 4
        unique_customers = (sessions['total_sessions'] / 12) / avg_sessions_per_customer_monthly
        members = unique_customers * self.revenue.percent_members
        membership_revenue = members * self.revenue.membership_monthly_fee * 12

        return {
            'idle_fee_revenue': idle_revenue,
            'membership_revenue': membership_revenue,
            'total_additional_revenue': idle_revenue + membership_revenue
        }

    def calculate_total_annual_revenue(self) -> Dict[str, float]:
        """Calculate total annual revenue from all sources."""
        charging_rev = self.calculate_charging_revenue()
        additional_rev = self.calculate_additional_revenue()

        return {
            'charging_revenue': charging_rev['total_charging_revenue'],
            'idle_fees': additional_rev['idle_fee_revenue'],
            'memberships': additional_rev['membership_revenue'],
            'total_revenue': (
                charging_rev['total_charging_revenue'] +
                additional_rev['total_additional_revenue']
            )
        }

    def calculate_electricity_costs(self) -> Dict[str, float]:
        """Calculate electricity costs by usage tier."""
        charging_data = self.calculate_charging_revenue()

        peak_cost = charging_data['peak_kwh'] * self.revenue.electricity_rate_peak
        standard_cost = charging_data['standard_kwh'] * self.revenue.electricity_rate_standard
        off_peak_cost = charging_data['off_peak_kwh'] * self.revenue.electricity_rate_off_peak

        return {
            'peak_electricity_cost': peak_cost,
            'standard_electricity_cost': standard_cost,
            'off_peak_electricity_cost': off_peak_cost,
            'total_electricity_cost': peak_cost + standard_cost + off_peak_cost
        }

    def calculate_total_annual_costs(self) -> Dict[str, float]:
        """Calculate total annual operating costs."""
        electricity = self.calculate_electricity_costs()
        fixed_costs = self.operating.total_fixed()

        return {
            'electricity_costs': electricity['total_electricity_cost'],
            'fixed_operating_costs': fixed_costs,
            'total_annual_costs': electricity['total_electricity_cost'] + fixed_costs
        }

    def calculate_annual_profit(self) -> float:
        """Calculate annual net profit."""
        revenue = self.calculate_total_annual_revenue()
        costs = self.calculate_total_annual_costs()
        return revenue['total_revenue'] - costs['total_annual_costs']

    def calculate_roi_metrics(self) -> Dict[str, float]:
        """Calculate ROI and payback metrics."""
        initial_investment = self.calculate_total_initial_investment()['total']
        annual_profit = self.calculate_annual_profit()

        roi = (annual_profit / initial_investment * 100) if initial_investment > 0 else 0
        payback = (initial_investment / annual_profit) if annual_profit > 0 else float('inf')

        # Multi-year projections
        year_5_total = (annual_profit * 5) - initial_investment
        year_10_total = (annual_profit * 10) - initial_investment

        return {
            'roi_percentage': roi,
            'payback_period_years': payback,
            'year_5_cumulative_profit': year_5_total,
            'year_10_cumulative_profit': year_10_total
        }

    def generate_comprehensive_report(self) -> Dict:
        """Generate complete financial report."""
        return {
            'initial_investment': self.calculate_total_initial_investment(),
            'annual_revenue': self.calculate_total_annual_revenue(),
            'annual_costs': self.calculate_total_annual_costs(),
            'annual_profit': self.calculate_annual_profit(),
            'electricity_breakdown': self.calculate_electricity_costs(),
            'charging_revenue_detail': self.calculate_charging_revenue(),
            'additional_revenue': self.calculate_additional_revenue(),
            'roi_metrics': self.calculate_roi_metrics(),
            'sessions_breakdown': self.calculate_annual_sessions()
        }

    def print_report(self):
        """Print formatted comprehensive report."""
        report = self.generate_comprehensive_report()

        print("=" * 80)
        print("COMPREHENSIVE TESLA SUPERCHARGER PROFITABILITY ANALYSIS")
        print("=" * 80)

        print(f"\n{'INITIAL INVESTMENT BREAKDOWN':-^80}")
        inv = report['initial_investment']
        print(f"  Installation Costs:          ${inv['installation']:>15,.2f}")
        print(f"  Equipment Costs:             ${inv['equipment']:>15,.2f}")
        print(f"  Licensing & Legal:           ${inv['licensing_legal']:>15,.2f}")
        print(f"  {'─' * 50}")
        print(f"  TOTAL INITIAL INVESTMENT:    ${inv['total']:>15,.2f}")

        print(f"\n{'ANNUAL REVENUE BREAKDOWN':-^80}")
        rev = report['annual_revenue']
        print(f"  Charging Revenue:            ${rev['charging_revenue']:>15,.2f}")
        print(f"  Idle Fee Revenue:            ${rev['idle_fees']:>15,.2f}")
        print(f"  Membership Revenue:          ${rev['memberships']:>15,.2f}")
        print(f"  {'─' * 50}")
        print(f"  TOTAL ANNUAL REVENUE:        ${rev['total_revenue']:>15,.2f}")

        print(f"\n{'ANNUAL COST BREAKDOWN':-^80}")
        costs = report['annual_costs']
        print(f"  Electricity Costs:           ${costs['electricity_costs']:>15,.2f}")
        print(f"  Fixed Operating Costs:       ${costs['fixed_operating_costs']:>15,.2f}")
        print(f"  {'─' * 50}")
        print(f"  TOTAL ANNUAL COSTS:          ${costs['total_annual_costs']:>15,.2f}")

        print(f"\n{'PROFITABILITY METRICS':-^80}")
        print(f"  Annual Net Profit:           ${report['annual_profit']:>15,.2f}")
        roi = report['roi_metrics']
        print(f"  Return on Investment (ROI):  {roi['roi_percentage']:>15.2f}%")

        if roi['payback_period_years'] == float('inf'):
            print(f"  Payback Period:              {'Never':>15}")
        else:
            print(f"  Payback Period:              {roi['payback_period_years']:>15.2f} years")

        print(f"  5-Year Cumulative Profit:    ${roi['year_5_cumulative_profit']:>15,.2f}")
        print(f"  10-Year Cumulative Profit:   ${roi['year_10_cumulative_profit']:>15,.2f}")

        print(f"\n{'USAGE STATISTICS':-^80}")
        sessions = report['sessions_breakdown']
        print(f"  Total Annual Sessions:       {sessions['total_sessions']:>15,.0f}")
        print(f"  Peak Hour Sessions:          {sessions['peak_sessions']:>15,.0f}")
        print(f"  Standard Hour Sessions:      {sessions['standard_sessions']:>15,.0f}")
        print(f"  Off-Peak Sessions:           {sessions['off_peak_sessions']:>15,.0f}")

        print("\n" + "=" * 80)

        # Recommendation
        if report['annual_profit'] > 0 and roi['payback_period_years'] < 5:
            print("RECOMMENDATION: ✓✓ Excellent investment opportunity")
        elif report['annual_profit'] > 0 and roi['payback_period_years'] < 7:
            print("RECOMMENDATION: ✓ Good investment opportunity")
        elif report['annual_profit'] > 0:
            print("RECOMMENDATION: ⚠ Marginal - Long payback period")
        else:
            print("RECOMMENDATION: ✗ Not profitable with current parameters")

        print("=" * 80)


def main():
    """Example usage with default parameters."""
    calculator = EnhancedSuperchargerCalculator()
    calculator.print_report()


if __name__ == '__main__':
    main()
