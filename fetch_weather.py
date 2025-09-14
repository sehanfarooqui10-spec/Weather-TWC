import requests
import os
import json
from datetime import datetime
from collections import defaultdict, Counter

API_KEY = os.getenv("TWC_API_KEY")

# TWC API endpoint for Karachi
API_URL = f"https://api.weather.com/v3/wx/forecast/hourly/15day?geocode=24.860735,67.001137&format=json&units=m&language=en-US&apiKey={API_KEY}"

def fetch_weather_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def process_daily_summary(data):
    grouped = defaultdict(list)

    times = data.get("validTimeLocal", [])
    temps = data.get("temperature", [])
    feels = data.get("temperatureFeelsLike", [])
    precip = data.get("precipChance", [])
 #   descs = data.get("narrative", [])

    # Group by date
    for i in range(len(times)):
        time_str = times[i]
        date_str = time_str.split("T")[0]  # YYYY-MM-DD
        grouped[date_str].append({
            "temp": temps[i],
            "feels": feels[i],
            "precip": precip[i],
     #       "desc": descs[i]
        })

    daily_summary = []
    for date, records in grouped.items():
        temps_list = [r["temp"] for r in records if r["temp"] is not None]
        feels_list = [r["feels"] for r in records if r["feels"] is not None]
        precip_list = [r["precip"] for r in records if r["precip"] is not None]
      #  desc_list = [r["desc"] for r in records if r["desc"]]

        if not temps_list:
            continue  # skip day if no data

        summary = {
            "date": date,
            "min_temp": min(temps_list),
            "max_temp": max(temps_list),
            "avg_feels_like": round(sum(feels_list) / len(feels_list), 1) if feels_list else None,
            "total_precip_chance": sum(precip_list) if precip_list else 0,
         #   "most_common_description": Counter(desc_list).most_common(1)[0][0] if desc_list else ""
        }
        daily_summary.append(summary)

    return daily_summary

def save_json(output):
    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

def main():
    data = fetch_weather_data()
    summary = process_daily_summary(data)

    output = {
        "location": "Karachi",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "daily_summary": summary
    }

    save_json(output)

if __name__ == "__main__":
    main()
