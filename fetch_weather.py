import requests
import os
import json
from datetime import datetime
from collections import defaultdict, Counter

API_KEY = os.getenv("TWC_API_KEY")

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
   # descs = data.get("narrative", [])

    for i in range(len(times)):
        date = times[i].split("T")[0]
        grouped[date].append({
            "temp": temps[i],
            "feels": feels[i],
            "precip": precip[i],
      #      "desc": descs[i]
        })

    summary = []
    for date, records in grouped.items():
        temps_list = [r["temp"] for r in records if r["temp"] is not None]
        feels_list = [r["feels"] for r in records if r["feels"] is not None]
        precip_list = [r["precip"] for r in records if r["precip"] is not None]
     #   desc_list = [r["desc"] for r in records if r["desc"]]

        if not temps_list:
            continue

        summary.append({
            "date": date,
            "min_temp": min(temps_list),
            "max_temp": max(temps_list),
            "avg_feels_like": round(sum(feels_list)/len(feels_list), 1) if feels_list else None,
            "total_precip_chance": sum(precip_list) if precip_list else 0,
        #    "most_common_description": Counter(desc_list).most_common(1)[0][0] if desc_list else ""
        })

    return summary

def save_json(location, updated_at, summary):
    output = {
        "location": location,
        "updated_at": updated_at,
        "daily_summary": summary
    }
    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

def save_html(location, updated_at, summary):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{location} Weather Summary</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        caption {{ font-size: 1.5em; margin-bottom: 10px; }}
    </style>
</head>
<body>
    <h1>{location} - 15-Day Weather Summary</h1>
    <p><strong>Last Updated:</strong> {updated_at}</p>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Min Temp (°C)</th>
                <th>Max Temp (°C)</th>
                <th>Avg Feels Like (°C)</th>
                <th>Total Precip (%)</th>
            </tr>
        </thead>
        <tbody>
    """

    for day in summary:
        html += f"""
            <tr>
                <td>{day["date"]}</td>
                <td>{day["min_temp"]}</td>
                <td>{day["max_temp"]}</td>
                <td>{day["avg_feels_like"]}</td>
                <td>{day["total_precip_chance"]}</td>
            </tr>
        """

    html += """
        </tbody>
    </table>
    <p style="margin-top:20px;">Data source: The Weather Channel API</p>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    location = "Karachi"
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = fetch_weather_data()
    summary = process_daily_summary(data)

    save_json(location, updated_at, summary)
    save_html(location, updated_at, summary)

if __name__ == "__main__":
    main()
