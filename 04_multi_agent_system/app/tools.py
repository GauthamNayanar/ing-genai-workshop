# tools.py
import json
from pathlib import Path

def load_mock_data():
    data_dir = Path(__file__).parent / "data"

    with open(data_dir / "mock_weather.json", "r", encoding="utf-8") as file:
        weather_data = json.load(file)

    with open(data_dir / "mock_flights.json", "r", encoding="utf-8") as file:
        flight_data = json.load(file)

    print("Mock data loaded.")
    return weather_data, flight_data


weather_data, flight_data = load_mock_data()


def normalize_city(city: str) -> str:
    """Normalize a city name for mock data lookup."""
    return " ".join(city.strip().split()).title()


def get_weather(location: str) -> dict:
    """Mock tool to get weather information for a given location."""
    print(f"🔧 TOOL CALLED: get_weather(location={location})")
    normalized_location = normalize_city(location)
    return weather_data.get(
        normalized_location,
        {"error": f"No mock weather found for {normalized_location}."},
    )


def search_flights(origin: str, destination: str) -> list:
    """Mock tool to search for flights between an origin and destination."""
    print(f"🔧 TOOL CALLED: search_flights(origin={origin}, destination={destination})")
    route = f"{normalize_city(origin)}-{normalize_city(destination)}"
    return flight_data.get(route, [])


def estimate_daily_budget(city: str, style: str) -> dict:
    """Estimate a mock daily budget for a city and travel style.

    Args:
        city: Destination city, for example Lisbon.
        style: Travel style: student, standard, or business.
    """
    normalized_city = normalize_city(city)
    normalized_style = style.strip().lower()

    base_costs = {
        "student": 65,
        "standard": 140,
        "business": 230,
    }
    city_multipliers = {
        "Amsterdam": 1.2,
        "Barcelona": 1.0,
        "Berlin": 1.0,
        "Lisbon": 0.85,
        "Tokyo": 1.3,
    }

    if normalized_style not in base_costs:
        return {
            "city": normalized_city,
            "style": style,
            "error": "Unknown style. Use student, standard, or business.",
        }

    estimated_daily_budget_eur = round(
        base_costs[normalized_style] * city_multipliers.get(normalized_city, 1.0),
        2,
    )

    return {
        "city": normalized_city,
        "style": normalized_style,
        "estimated_daily_budget_eur": estimated_daily_budget_eur,
        "includes": ["meals", "local transport", "basic activities"],
    }


def check_trip_conflicts(weather_report: str, flight_report: str, budget_report: str) -> dict:
    """Exercise 5: identify conflicts between specialist reports."""
    # TODO: inspect the text reports and return risks, conflicts, and missing data.
    return {
        "weather_report": weather_report,
        "flight_report": flight_report,
        "budget_report": budget_report,
        "todo": "Identify conflicts and missing data across specialist outputs.",
    }
