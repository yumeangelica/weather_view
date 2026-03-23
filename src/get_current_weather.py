"""Fetch current weather data from OpenWeatherMap API."""

from datetime import datetime
import requests
import pytz

from src.uv_calculator import estimate_uv_index
from src.config_loader import load_config


def get_weather_with_uv(api_key: str, city: str) -> dict | None:
    """Fetch current weather for a city, including estimated UV index.

    Args:
        api_key: OpenWeatherMap API key.
        city: City name to query.

    Returns:
        Dictionary with weather data, or None on failure.
    """
    if not api_key or not api_key.strip():
        print("Error: Invalid API key provided.")
        return None

    config = load_config()
    api = config['api']
    display = config['display']
    uv_peak = config['uv']['peak_value']

    url = f"{api['base_url']}{api['current_endpoint']}"
    params = {"q": city, "appid": api_key, "units": api['units']}

    try:
        resp = requests.get(url, params=params, timeout=api['timeout'])
        data = resp.json()

        if resp.status_code != 200:
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # Build local timezone from API offset
        tz_offset = data.get("timezone", 0)
        local_tz = pytz.FixedOffset(tz_offset // 60)

        # Estimate UV index from solar position
        current_time_utc = datetime.now(tz=pytz.utc)
        uv_value = estimate_uv_index(lat, lon, current_time_utc, uv_peak)

        # Format sunrise/sunset in local time
        dt_format = display['datetime_format']
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
            "sunrise": sunrise.strftime(dt_format),
            "sunset": sunset.strftime(dt_format),
            "icon": data["weather"][0]["icon"],
            "uv_index": uv_value,
            "cloudiness": data["clouds"]["all"],
            "pressure": data["main"]["pressure"],
            "visibility": data.get("visibility", "N/A"),
            "rain": data.get("rain", {}).get("1h", "0 mm"),
            "snow": data.get("snow", {}).get("1h", "0 mm"),
        }

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again later.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the weather service.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Network request failed: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error: Unexpected response format: {e}")
        return None