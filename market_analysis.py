"""
US Market Analysis for Tesla Supercharger Placement

Analyzes charger density vs population density to identify
underserved and oversaturated markets.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


# Major US Metropolitan Areas with Population Data (2023 estimates)
US_METRO_AREAS = [
    # Name, State, Lat, Lon, Population, Existing_Chargers
    ("New York", "NY", 40.7128, -74.0060, 8336817, 45),
    ("Los Angeles", "CA", 34.0522, -118.2437, 3898747, 52),
    ("Chicago", "IL", 41.8781, -87.6298, 2746388, 28),
    ("Houston", "TX", 29.7604, -95.3698, 2304580, 25),
    ("Phoenix", "AZ", 33.4484, -112.0740, 1608139, 18),
    ("Philadelphia", "PA", 39.9526, -75.1652, 1603797, 15),
    ("San Antonio", "TX", 29.4241, -98.4936, 1434625, 12),
    ("San Diego", "CA", 32.7157, -117.1611, 1386932, 22),
    ("Dallas", "TX", 32.7767, -96.7970, 1304379, 24),
    ("San Jose", "CA", 37.3382, -121.8863, 1013240, 28),
    ("Austin", "TX", 30.2672, -97.7431, 961855, 16),
    ("Jacksonville", "FL", 30.3322, -81.6557, 949611, 8),
    ("Fort Worth", "TX", 32.7555, -97.3308, 918915, 10),
    ("Columbus", "OH", 39.9612, -82.9988, 905748, 9),
    ("Charlotte", "NC", 35.2271, -80.8431, 897720, 11),
    ("San Francisco", "CA", 37.7749, -122.4194, 873965, 35),
    ("Indianapolis", "IN", 39.7684, -86.1581, 887642, 8),
    ("Seattle", "WA", 47.6062, -122.3321, 749256, 30),
    ("Denver", "CO", 39.7392, -104.9903, 715522, 20),
    ("Washington", "DC", 38.9072, -77.0369, 712816, 25),
    ("Boston", "MA", 42.3601, -71.0589, 675647, 22),
    ("Nashville", "TN", 36.1627, -86.7816, 689447, 10),
    ("Detroit", "MI", 42.3314, -83.0458, 639111, 12),
    ("Oklahoma City", "OK", 35.4676, -97.5164, 687725, 7),
    ("Portland", "OR", 45.5152, -122.6784, 652503, 18),
    ("Las Vegas", "NV", 36.1699, -115.1398, 656274, 15),
    ("Memphis", "TN", 35.1495, -90.0490, 633104, 6),
    ("Louisville", "KY", 38.2527, -85.7585, 633045, 5),
    ("Baltimore", "MD", 39.2904, -76.6122, 585708, 10),
    ("Milwaukee", "WI", 43.0389, -87.9065, 577222, 8),
    ("Albuquerque", "NM", 35.0844, -106.6504, 564559, 9),
    ("Tucson", "AZ", 32.2226, -110.9747, 548073, 8),
    ("Fresno", "CA", 36.7378, -119.7871, 542107, 6),
    ("Sacramento", "CA", 38.5816, -121.4944, 524943, 14),
    ("Kansas City", "MO", 39.0997, -94.5786, 508090, 9),
    ("Atlanta", "GA", 33.7490, -84.3880, 498715, 20),
    ("Miami", "FL", 25.7617, -80.1918, 449514, 18),
    ("Raleigh", "NC", 35.7796, -78.6382, 474069, 8),
    ("Omaha", "NE", 41.2565, -95.9345, 486051, 5),
    ("Colorado Springs", "CO", 38.8339, -104.8214, 478961, 7),
    ("Minneapolis", "MN", 44.9778, -93.2650, 425403, 15),
    ("Tampa", "FL", 27.9506, -82.4572, 398173, 12),
    ("Orlando", "FL", 28.5383, -81.3792, 307573, 14),
    ("Cleveland", "OH", 41.4993, -81.6944, 372624, 7),
    ("Boise", "ID", 43.6150, -116.2023, 235684, 6),
    ("Salt Lake City", "UT", 40.7608, -111.8910, 200567, 12),
    ("Buffalo", "NY", 42.8864, -78.8784, 276807, 5),
    ("Pittsburgh", "PA", 40.4406, -79.9959, 302971, 8),
    ("Cincinnati", "OH", 39.1031, -84.5120, 309317, 7),
    ("Anchorage", "AK", 61.2181, -149.9003, 291247, 3),
    ("St. Louis", "MO", 38.6270, -90.1994, 301578, 10),
    # Add more mid-size cities for better coverage
    ("Madison", "WI", 43.0731, -89.4012, 269840, 5),
    ("Des Moines", "IA", 41.6005, -93.6091, 214133, 4),
    ("Richmond", "VA", 37.5407, -77.4360, 230436, 6),
    ("Charleston", "SC", 32.7765, -79.9311, 150227, 4),
    ("Birmingham", "AL", 33.5186, -86.8104, 200733, 5),
    ("New Orleans", "LA", 29.9511, -90.0715, 383997, 6),
    ("Little Rock", "AR", 34.7465, -92.2896, 202591, 3),
    ("Spokane", "WA", 47.6588, -117.4260, 228989, 5),
    ("Fargo", "ND", 46.8772, -96.7898, 125990, 2),
    ("Sioux Falls", "SD", 43.5460, -96.7313, 192517, 3),
]


class MarketAnalyzer:
    """Analyze US markets for Supercharger profitability."""

    def __init__(self):
        self.df = self._create_dataframe()
        self._calculate_metrics()

    def _create_dataframe(self) -> pd.DataFrame:
        """Create DataFrame from metro area data."""
        return pd.DataFrame(
            US_METRO_AREAS,
            columns=['city', 'state', 'lat', 'lon', 'population', 'chargers']
        )

    def _calculate_metrics(self):
        """Calculate density and gap metrics."""
        # People per charger (lower is better coverage)
        self.df['people_per_charger'] = self.df['population'] / self.df['chargers']

        # Chargers per 100k people (higher is better coverage)
        self.df['chargers_per_100k'] = (self.df['chargers'] / self.df['population']) * 100000

        # Market size score (larger cities = more potential)
        self.df['market_size_score'] = self.df['population'] / self.df['population'].max() * 100

        # Calculate national average
        avg_chargers_per_100k = (self.df['chargers'].sum() / self.df['population'].sum()) * 100000

        # Gap analysis (negative = underserved, positive = oversaturated)
        self.df['coverage_gap'] = self.df['chargers_per_100k'] - avg_chargers_per_100k

        # Opportunity score (higher = better opportunity)
        # Based on: high population + low charger density
        self.df['opportunity_score'] = (
            (self.df['market_size_score'] / 100) *  # Larger market
            (1 / (self.df['chargers_per_100k'] / avg_chargers_per_100k))  # Lower coverage
        ) * 100

    def get_market_data(self) -> pd.DataFrame:
        """Get the full market analysis DataFrame."""
        return self.df.copy()

    def get_top_opportunities(self, n: int = 10) -> pd.DataFrame:
        """Get top N underserved markets with best opportunity."""
        return self.df.nlargest(n, 'opportunity_score')[
            ['city', 'state', 'population', 'chargers', 'people_per_charger',
             'chargers_per_100k', 'coverage_gap', 'opportunity_score']
        ]

    def get_oversaturated_markets(self, n: int = 10) -> pd.DataFrame:
        """Get markets with highest charger density (potentially oversaturated)."""
        return self.df.nlargest(n, 'chargers_per_100k')[
            ['city', 'state', 'population', 'chargers', 'people_per_charger',
             'chargers_per_100k', 'coverage_gap']
        ]

    def get_underserved_markets(self, n: int = 10) -> pd.DataFrame:
        """Get markets with lowest charger density (underserved)."""
        return self.df.nsmallest(n, 'chargers_per_100k')[
            ['city', 'state', 'population', 'chargers', 'people_per_charger',
             'chargers_per_100k', 'coverage_gap', 'opportunity_score']
        ]

    def get_national_stats(self) -> Dict:
        """Get national-level statistics."""
        return {
            'total_population': self.df['population'].sum(),
            'total_chargers': self.df['chargers'].sum(),
            'avg_chargers_per_100k': (self.df['chargers'].sum() /
                                      self.df['population'].sum()) * 100000,
            'avg_people_per_charger': self.df['people_per_charger'].mean(),
            'median_people_per_charger': self.df['people_per_charger'].median(),
            'cities_analyzed': len(self.df)
        }

    def classify_market(self, city: str, state: str) -> str:
        """Classify a market as underserved, balanced, or oversaturated."""
        market = self.df[(self.df['city'] == city) & (self.df['state'] == state)]

        if market.empty:
            return "Unknown"

        gap = market.iloc[0]['coverage_gap']

        if gap < -0.5:
            return "Underserved (High Opportunity)"
        elif gap > 0.5:
            return "Oversaturated"
        else:
            return "Balanced"

    def get_regional_analysis(self) -> pd.DataFrame:
        """Group markets by region for analysis."""
        # Define US regions
        regions = {
            'Northeast': ['NY', 'PA', 'MA', 'MD', 'DC'],
            'Southeast': ['FL', 'GA', 'NC', 'SC', 'TN', 'KY', 'LA', 'AL'],
            'Midwest': ['IL', 'OH', 'MI', 'WI', 'MN', 'MO', 'IN', 'IA', 'ND', 'SD', 'NE', 'KS'],
            'Southwest': ['TX', 'AZ', 'NM', 'OK', 'AR'],
            'West': ['CA', 'WA', 'OR', 'NV', 'CO', 'UT', 'ID', 'AK']
        }

        # Map states to regions
        def get_region(state):
            for region, states in regions.items():
                if state in states:
                    return region
            return 'Other'

        self.df['region'] = self.df['state'].apply(get_region)

        # Regional aggregation
        regional = self.df.groupby('region').agg({
            'population': 'sum',
            'chargers': 'sum',
            'city': 'count'
        }).rename(columns={'city': 'cities'})

        regional['chargers_per_100k'] = (regional['chargers'] / regional['population']) * 100000
        regional['people_per_charger'] = regional['population'] / regional['chargers']

        return regional.sort_values('chargers_per_100k', ascending=False)


def generate_sample_locations_for_heatmap(num_points: int = 500) -> pd.DataFrame:
    """
    Generate additional sample charger locations for smoother heat map visualization.
    This creates interpolated points around actual charger locations.
    """
    analyzer = MarketAnalyzer()
    df = analyzer.get_market_data()

    all_points = []

    for _, row in df.iterrows():
        # Add actual location
        all_points.append({
            'lat': row['lat'],
            'lon': row['lon'],
            'type': 'actual',
            'chargers': row['chargers'],
            'city': row['city']
        })

        # Add nearby points with decreasing density (for heat map effect)
        num_nearby = int(row['chargers'] / 2)
        for _ in range(num_nearby):
            all_points.append({
                'lat': row['lat'] + np.random.normal(0, 0.3),
                'lon': row['lon'] + np.random.normal(0, 0.3),
                'type': 'interpolated',
                'chargers': 1,
                'city': row['city']
            })

    return pd.DataFrame(all_points)


if __name__ == '__main__':
    # Example usage
    analyzer = MarketAnalyzer()

    print("=" * 80)
    print("US SUPERCHARGER MARKET ANALYSIS")
    print("=" * 80)

    stats = analyzer.get_national_stats()
    print(f"\nNational Statistics:")
    print(f"  Total Population (analyzed): {stats['total_population']:,}")
    print(f"  Total Chargers: {stats['total_chargers']:,}")
    print(f"  Avg Chargers per 100k people: {stats['avg_chargers_per_100k']:.2f}")
    print(f"  Avg People per Charger: {stats['avg_people_per_charger']:,.0f}")

    print(f"\n{'TOP 10 OPPORTUNITIES (Underserved Markets)':-^80}")
    opportunities = analyzer.get_top_opportunities(10)
    for idx, row in opportunities.iterrows():
        print(f"{row['city']}, {row['state']:<2} | "
              f"Pop: {row['population']:>8,} | "
              f"Chargers: {row['chargers']:>3} | "
              f"Per 100k: {row['chargers_per_100k']:>5.2f} | "
              f"Opportunity: {row['opportunity_score']:>5.1f}")

    print(f"\n{'MOST OVERSATURATED MARKETS':-^80}")
    oversaturated = analyzer.get_oversaturated_markets(5)
    for idx, row in oversaturated.iterrows():
        print(f"{row['city']}, {row['state']:<2} | "
              f"Pop: {row['population']:>8,} | "
              f"Chargers: {row['chargers']:>3} | "
              f"Per 100k: {row['chargers_per_100k']:>5.2f}")

    print(f"\n{'REGIONAL ANALYSIS':-^80}")
    regional = analyzer.get_regional_analysis()
    print(regional.to_string())

    print("\n" + "=" * 80)
