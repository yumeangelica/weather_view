from datetime import datetime
import requests
import math
import pytz
from pysolar.solar import get_altitude

UV_PEAK = 8.0  # Estimated daily peak UV value

def get_forecast(openweathermap_api_key: str, city: str):
    if not openweathermap_api_key or not openweathermap_api_key.strip():
        print("Error: Invalid API key provided")
        return None

    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": openweathermap_api_key, "units": "metric", "cnt": 24}
    resp = requests.get(url, params=params)
    data = resp.json()
    if resp.status_code != 200:
        print(f"API error (forecast): {data.get('message','Unknown error')}")
        return None

    coord = data["city"]["coord"]
    lat, lon = coord["lat"], coord["lon"]
    tz_offset = data["city"].get("timezone", 0)
    local_tz = pytz.FixedOffset(tz_offset // 60)

    forecasts = []
    for item in data["list"]:
        ts = item["dt"]

        # UTC timestamp for UV calculation
        dt_utc = datetime.fromtimestamp(ts, tz=pytz.utc)
        altitude_deg = get_altitude(lat, lon, dt_utc)
        if altitude_deg > 0:
            uv_val = round(UV_PEAK * math.sin(math.radians(altitude_deg)), 2)
        else:
            uv_val = 0.0

        # Convert to local timezone
        dt_local = datetime.fromtimestamp(ts, tz=local_tz)
        dt_str = dt_local.strftime("%Y-%m-%d %H:%M:%S %Z")

        forecasts.append({
            "datetime": dt_str,
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"],
            "icon": item["weather"][0]["icon"],
            "uv_index": uv_val
        })

    return forecasts
