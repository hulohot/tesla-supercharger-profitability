# Tesla Supercharger Profitability Calculator

Determine the profitability parameters for individuals or businesses to white-label Tesla Superchargers.

## Overview

This calculator helps analyze the financial viability of installing and operating Tesla Supercharger stations. It calculates key metrics including:

- Initial investment costs
- Annual revenue projections
- Operating expenses
- Net profit
- Return on Investment (ROI)
- Payback period
- 5-year profit projections

## Installation

No external dependencies required! Just Python 3.6+

```bash
chmod +x calculator.py
```

## Usage

### Basic Usage (Default Parameters)

```bash
python3 calculator.py
```

This runs the calculator with default parameters:
- 8 charging stalls
- $35,000 equipment cost per stall
- $100,000 installation cost
- $25,000 permitting fees
- $24,000/year land lease
- $0.15/kWh electricity cost
- $0.35/kWh charging price to customers
- 70% utilization rate

### Custom Parameters

Customize any parameter using command-line arguments:

```bash
python3 calculator.py --stalls 12 --charging-price 0.40 --utilization 0.85
```

### Available Options

```
--stalls                Number of charging stalls (default: 8)
--equipment-cost        Equipment cost per stall in USD (default: 35000)
--installation          Total installation cost in USD (default: 100000)
--permitting            Permitting fees in USD (default: 25000)
--land-lease            Annual land lease cost in USD (default: 24000)
--electricity-rate      Cost per kWh of electricity in USD (default: 0.15)
--maintenance           Annual maintenance cost in USD (default: 15000)
--charging-price        Price charged per kWh in USD (default: 0.35)
--kwh-per-session       Average kWh per charging session (default: 50)
--sessions-per-day      Average sessions per stall per day (default: 5)
--utilization           Utilization rate 0-1 (default: 0.70)
```

## Example Scenarios

### High-Traffic Location
```bash
python3 calculator.py --stalls 12 --sessions-per-day 8 --utilization 0.85
```

### Budget Installation
```bash
python3 calculator.py --stalls 4 --installation 50000 --permitting 10000
```

### Premium Pricing Model
```bash
python3 calculator.py --charging-price 0.45 --electricity-rate 0.12
```

## Using as a Library

You can also import the calculator in your Python code:

```python
from calculator import SuperchargerProfitabilityCalculator

calc = SuperchargerProfitabilityCalculator(
    num_stalls=10,
    charging_price_kwh=0.40,
    utilization_rate=0.80
)

report = calc.generate_report()
print(f"Annual Profit: ${report['annual_profit']:,.2f}")
print(f"ROI: {report['roi_percentage']:.2f}%")
print(f"Payback Period: {report['payback_period_years']:.2f} years")
```

## Understanding the Metrics

- **Initial Investment**: Total upfront costs including equipment, installation, and permitting
- **Annual Revenue**: Expected yearly income from charging sessions
- **Annual Operating Costs**: Yearly expenses including electricity, land lease, and maintenance
- **Annual Net Profit**: Revenue minus operating costs
- **ROI (Return on Investment)**: Annual profit as a percentage of initial investment
- **Payback Period**: Years needed to recover the initial investment
- **5-Year Total Profit**: Net profit over 5 years (after recovering initial investment)

## License

See LICENSE file for details.
