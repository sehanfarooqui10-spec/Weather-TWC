import requests
import os
import json
from datetime import datetime

# Use environment variable for security
API_KEY = os.getenv("TWC_API_KEY")

# TWC API endpoint for Karachi
API_URL = f"https://api.weather.com/v3/wx/forecast/hourly/15day?geocode=24.860735,67.001137&format=json&units=m&language=en-US&apiKey={API_KEY}"

def fetch_and_format_weather():
    response = requests.get(API_URL)
    data = response.json()

    # Get the first 12 forecast hours
    forecast = []
    for i in range(min(12, len(data.get("validTimeLocal", [])))):
        forecast.append({
            "time": data["validTimeLocal"][i],
            "temperature": data["temperature"][i],
            "feels_like": data["temperatureFeelsLike"][i],
            "precipitation_chance": data["precipChance"][i],
           ## "description": data["narrative"][i]
        })

    # Build final flat structure
    output = {
        "location": "Karachi",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "forecast": forecast
    }

    # Save to JSON file
    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    fetch_and_format_weather()
