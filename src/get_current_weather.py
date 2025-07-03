import requests
from datetime import datetime
import pytz
import math
from pysolar.solar import get_altitude

UV_PEAK = 8.0  # Estimated daily peak UV value

def get_weather_with_uv(openweathermap_api_key: str, city: str):
    if not openweathermap_api_key or not openweathermap_api_key.strip():
        print("Error: Invalid API key provided")
        return None

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": openweathermap_api_key, "units": "metric"}

    try:
        resp = requests.get(url, params=params)
        data = resp.json()

        if resp.status_code != 200:
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        tz_offset = data.get("timezone", 0)
        local_tz = pytz.FixedOffset(tz_offset // 60)        # Calculate UV index using solar position at current local time
        current_time_local = datetime.now(tz=local_tz)
        current_time_utc = current_time_local.astimezone(pytz.utc)
        altitude_deg = get_altitude(lat, lon, current_time_utc)

        if altitude_deg > 0:
            uv_value = round(UV_PEAK * math.sin(math.radians(altitude_deg)), 2)
        else:
            uv_value = 0.0

        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz=local_tz)
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz=local_tz)

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_max": data["main"]["temp_max"],
            "temp_min": data["main"]["temp_min"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "sunrise": sunrise.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "sunset": sunset.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "icon": data["weather"][0]["icon"],
            "uv_index": uv_value,
            "cloudiness": data["clouds"]["all"],
            "pressure": data["main"]["pressure"],
            "visibility": data.get("visibility", "N/A"),
            "rain": data.get("rain", {}).get("1h", "0 mm"),
            "snow": data.get("snow", {}).get("1h", "0 mm"),
        }
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return None
