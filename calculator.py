#!/usr/bin/env python3
"""
Tesla Supercharger Profitability Calculator

This calculator helps determine the financial viability of white-labeling
Tesla Superchargers by analyzing initial costs, operational expenses, revenue,
and profitability metrics.
"""

import argparse
from typing import Dict, Tuple


class SuperchargerProfitabilityCalculator:
    """
    Calculate profitability metrics for Tesla Supercharger installations.
    """

    def __init__(
        self,
        num_stalls: int = 8,
        equipment_cost_per_stall: float = 35000,
        installation_cost: float = 100000,
        permitting_fees: float = 25000,
        land_lease_annual: float = 24000,
        electricity_rate_kwh: float = 0.15,
        maintenance_annual: float = 15000,
        charging_price_kwh: float = 0.35,
        avg_kwh_per_session: float = 50,
        sessions_per_stall_per_day: float = 5,
        utilization_rate: float = 0.70
    ):
        """
        Initialize the calculator with financial parameters.

        Args:
            num_stalls: Number of charging stalls
            equipment_cost_per_stall: Cost per stall in USD
            installation_cost: Total installation cost in USD
            permitting_fees: Permitting and legal fees in USD
            land_lease_annual: Annual land lease cost in USD
            electricity_rate_kwh: Cost per kWh of electricity in USD
            maintenance_annual: Annual maintenance cost in USD
            charging_price_kwh: Price charged to customers per kWh in USD
            avg_kwh_per_session: Average kWh delivered per charging session
            sessions_per_stall_per_day: Average sessions per stall per day
            utilization_rate: Percentage of time stalls are utilized (0-1)
        """
        self.num_stalls = num_stalls
        self.equipment_cost_per_stall = equipment_cost_per_stall
        self.installation_cost = installation_cost
        self.permitting_fees = permitting_fees
        self.land_lease_annual = land_lease_annual
        self.electricity_rate_kwh = electricity_rate_kwh
        self.maintenance_annual = maintenance_annual
        self.charging_price_kwh = charging_price_kwh
        self.avg_kwh_per_session = avg_kwh_per_session
        self.sessions_per_stall_per_day = sessions_per_stall_per_day
        self.utilization_rate = utilization_rate

    def calculate_initial_investment(self) -> float:
        """Calculate total initial investment required."""
        equipment_total = self.num_stalls * self.equipment_cost_per_stall
        return equipment_total + self.installation_cost + self.permitting_fees

    def calculate_annual_revenue(self) -> float:
        """Calculate annual revenue from charging sessions."""
        sessions_per_year = (
            self.num_stalls *
            self.sessions_per_stall_per_day *
            365 *
            self.utilization_rate
        )
        kwh_per_year = sessions_per_year * self.avg_kwh_per_session
        return kwh_per_year * self.charging_price_kwh

    def calculate_annual_electricity_cost(self) -> float:
        """Calculate annual electricity cost."""
        sessions_per_year = (
            self.num_stalls *
            self.sessions_per_stall_per_day *
            365 *
            self.utilization_rate
        )
        kwh_per_year = sessions_per_year * self.avg_kwh_per_session
        return kwh_per_year * self.electricity_rate_kwh

    def calculate_annual_operating_costs(self) -> float:
        """Calculate total annual operating costs."""
        electricity_cost = self.calculate_annual_electricity_cost()
        return electricity_cost + self.land_lease_annual + self.maintenance_annual

    def calculate_annual_profit(self) -> float:
        """Calculate annual net profit."""
        revenue = self.calculate_annual_revenue()
        costs = self.calculate_annual_operating_costs()
        return revenue - costs

    def calculate_roi(self) -> float:
        """Calculate Return on Investment (ROI) as a percentage."""
        initial_investment = self.calculate_initial_investment()
        annual_profit = self.calculate_annual_profit()
        if initial_investment == 0:
            return 0
        return (annual_profit / initial_investment) * 100

    def calculate_payback_period(self) -> float:
        """Calculate payback period in years."""
        initial_investment = self.calculate_initial_investment()
        annual_profit = self.calculate_annual_profit()
        if annual_profit <= 0:
            return float('inf')
        return initial_investment / annual_profit

    def calculate_5year_profit(self) -> float:
        """Calculate total profit over 5 years."""
        annual_profit = self.calculate_annual_profit()
        initial_investment = self.calculate_initial_investment()
        return (annual_profit * 5) - initial_investment

    def generate_report(self) -> Dict[str, float]:
        """
        Generate a comprehensive profitability report.

        Returns:
            Dictionary containing all financial metrics
        """
        return {
            'initial_investment': self.calculate_initial_investment(),
            'annual_revenue': self.calculate_annual_revenue(),
            'annual_electricity_cost': self.calculate_annual_electricity_cost(),
            'annual_operating_costs': self.calculate_annual_operating_costs(),
            'annual_profit': self.calculate_annual_profit(),
            'roi_percentage': self.calculate_roi(),
            'payback_period_years': self.calculate_payback_period(),
            'five_year_profit': self.calculate_5year_profit()
        }

    def print_report(self):
        """Print a formatted profitability report."""
        report = self.generate_report()

        print("=" * 60)
        print("TESLA SUPERCHARGER PROFITABILITY ANALYSIS")
        print("=" * 60)
        print(f"\nConfiguration:")
        print(f"  Number of Stalls: {self.num_stalls}")
        print(f"  Utilization Rate: {self.utilization_rate * 100:.1f}%")
        print(f"  Charging Price: ${self.charging_price_kwh:.2f}/kWh")
        print(f"  Electricity Cost: ${self.electricity_rate_kwh:.2f}/kWh")

        print(f"\n{'INITIAL INVESTMENT':-^60}")
        print(f"  Total Initial Investment: ${report['initial_investment']:,.2f}")

        print(f"\n{'ANNUAL FINANCIALS':-^60}")
        print(f"  Annual Revenue: ${report['annual_revenue']:,.2f}")
        print(f"  Annual Electricity Cost: ${report['annual_electricity_cost']:,.2f}")
        print(f"  Annual Operating Costs: ${report['annual_operating_costs']:,.2f}")
        print(f"  Annual Net Profit: ${report['annual_profit']:,.2f}")

        print(f"\n{'PROFITABILITY METRICS':-^60}")
        print(f"  Return on Investment (ROI): {report['roi_percentage']:.2f}%")

        if report['payback_period_years'] == float('inf'):
            print(f"  Payback Period: Never (negative profit)")
        else:
            print(f"  Payback Period: {report['payback_period_years']:.2f} years")

        print(f"  5-Year Total Profit: ${report['five_year_profit']:,.2f}")

        print("\n" + "=" * 60)

        # Provide recommendation
        if report['annual_profit'] > 0 and report['payback_period_years'] < 7:
            print("RECOMMENDATION: ✓ Good investment opportunity")
        elif report['annual_profit'] > 0:
            print("RECOMMENDATION: ⚠ Marginal - Long payback period")
        else:
            print("RECOMMENDATION: ✗ Not profitable with current parameters")
        print("=" * 60)


def main():
    """Command-line interface for the calculator."""
    parser = argparse.ArgumentParser(
        description="Calculate profitability for Tesla Supercharger installations"
    )

    parser.add_argument(
        '--stalls', type=int, default=8,
        help='Number of charging stalls (default: 8)'
    )
    parser.add_argument(
        '--equipment-cost', type=float, default=35000,
        help='Equipment cost per stall in USD (default: 35000)'
    )
    parser.add_argument(
        '--installation', type=float, default=100000,
        help='Total installation cost in USD (default: 100000)'
    )
    parser.add_argument(
        '--permitting', type=float, default=25000,
        help='Permitting fees in USD (default: 25000)'
    )
    parser.add_argument(
        '--land-lease', type=float, default=24000,
        help='Annual land lease cost in USD (default: 24000)'
    )
    parser.add_argument(
        '--electricity-rate', type=float, default=0.15,
        help='Cost per kWh of electricity in USD (default: 0.15)'
    )
    parser.add_argument(
        '--maintenance', type=float, default=15000,
        help='Annual maintenance cost in USD (default: 15000)'
    )
    parser.add_argument(
        '--charging-price', type=float, default=0.35,
        help='Price charged per kWh in USD (default: 0.35)'
    )
    parser.add_argument(
        '--kwh-per-session', type=float, default=50,
        help='Average kWh per charging session (default: 50)'
    )
    parser.add_argument(
        '--sessions-per-day', type=float, default=5,
        help='Average sessions per stall per day (default: 5)'
    )
    parser.add_argument(
        '--utilization', type=float, default=0.70,
        help='Utilization rate 0-1 (default: 0.70)'
    )

    args = parser.parse_args()

    calculator = SuperchargerProfitabilityCalculator(
        num_stalls=args.stalls,
        equipment_cost_per_stall=args.equipment_cost,
        installation_cost=args.installation,
        permitting_fees=args.permitting,
        land_lease_annual=args.land_lease,
        electricity_rate_kwh=args.electricity_rate,
        maintenance_annual=args.maintenance,
        charging_price_kwh=args.charging_price,
        avg_kwh_per_session=args.kwh_per_session,
        sessions_per_stall_per_day=args.sessions_per_day,
        utilization_rate=args.utilization
    )

    calculator.print_report()


if __name__ == '__main__':
    main()
