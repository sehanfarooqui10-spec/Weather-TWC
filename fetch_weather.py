import requests
import os
from datetime import datetime

# Get the API key from environment variable (GitHub secret)
API_KEY = os.getenv("TWC_API_KEY")

# Define the TWC API endpoint
API_URL = f"https://api.weather.com/v3/wx/forecast/hourly/15day?geocode=24.860735,67.001137&format=json&units=m&language=en-US&apiKey={API_KEY}"

def fetch_weather():
    response = requests.get(API_URL)
    data = response.json()
    

    # Sample fields: extracting first 12 hours
    hours = data.get("validTimeLocal", [])[:12]
    print(hours)
    temps = data.get("temperature", [])[:12]
    feels_like = data.get("temperatureFeelsLike", [])[:12]
    precip = data.get("precipChance", [])[:12]
    #narrative = data.get("narrative", [])[:12]

    html = """
    <html>
    <head><title>Karachi Hourly Weather Forecast</title></head>
    <body>
    <h1>Hourly Weather Forecast (Karachi)</h1>
    <p><strong>Last updated:</strong> {}</p>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Time</th>
            <th>Temp (°C)</th>
            <th>Feels Like (°C)</th>
            <th>Precip (%)</th>
            <th>Description</th>
        </tr>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    for i in range(len(hours)):
        html += f"""
        <tr>
            <td>{hours[i]}</td>
            <td>{temps[i]}</td>
            <td>{feels_like[i]}</td>
            <td>{precip[i]}</td>
        </tr>
        """

    html += """
    </table>
    <p>Source: The Weather Channel API</p>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    fetch_weather()
