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


def get_weather(location: str) -> dict:
    """Mock tool to get weather information for a given location."""
    print(f"🔧 TOOL CALLED: get_weather(location={location})")
    return weather_data.get(location, {"error": f"No mock weather found for {location}."})


def search_flights(origin: str, destination: str) -> list:
    """Mock tool to search for flights between an origin and destination."""
    print(f"🔧 TOOL CALLED: search_flights(origin={origin}, destination={destination})")
    route = f"{origin}-{destination}"
    return flight_data.get(route, [])


def your_tool():
    """Define your own tool here!

    Ideas:
    - estimate_daily_budget(city, style)
    - suggest_airport_transfer(city)
    - get_visa_requirements(passport_country, destination_country)
    """
    pass