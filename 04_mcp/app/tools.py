# tools.py
import json
from pathlib import Path

def load_mock_data():
    data_dir = Path(__file__).parent / "data"

    with open(data_dir / "mock_weather.json", "r", encoding="utf-8") as file:
        weather_data = json.load(file)

    print("Mock data loaded.")
    return weather_data


WEATHER_DATA = load_mock_data()


def get_weather(location: str) -> dict:
    """Mock tool to get weather information for a given location."""
    print(f"🔧 TOOL CALLED: get_weather(location={location})")
    return WEATHER_DATA.get(location, {"error": f"No mock weather found for {location}."})
