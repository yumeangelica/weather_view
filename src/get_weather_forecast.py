"""Fetch weather forecast data from OpenWeatherMap API."""

from datetime import datetime
import requests
import pytz

from src.uv_calculator import estimate_uv_index
from src.config_loader import load_config


def get_forecast(api_key: str, city: str) -> list[dict] | None:
    """Fetch 3-day forecast for a city, including estimated UV index.

    Args:
        api_key: OpenWeatherMap API key.
        city: City name to query.

    Returns:
        List of forecast dictionaries, or None on failure.
    """
    if not api_key or not api_key.strip():
        print("Error: Invalid API key provided.")
        return None

    config = load_config()
    api = config['api']
    display = config['display']
    uv_peak = config['uv']['peak_value']

    url = f"{api['base_url']}{api['forecast_endpoint']}"
    params = {
        "q": city,
        "appid": api_key,
        "units": api['units'],
        "cnt": api['forecast_count']
    }

    try:
        resp = requests.get(url, params=params, timeout=api['timeout'])
        data = resp.json()

        if resp.status_code != 200:
            print(f"API error (forecast): {data.get('message', 'Unknown error')}")
            return None

        coord = data["city"]["coord"]
        lat, lon = coord["lat"], coord["lon"]
        tz_offset = data["city"].get("timezone", 0)
        local_tz = pytz.FixedOffset(tz_offset // 60)
        dt_format = display['datetime_format']

        forecasts = []
        for item in data["list"]:
            ts = item["dt"]

            # Calculate UV from solar position at forecast time
            dt_utc = datetime.fromtimestamp(ts, tz=pytz.utc)
            uv_val = estimate_uv_index(lat, lon, dt_utc, uv_peak)

            # Convert to local timezone for display
            dt_local = datetime.fromtimestamp(ts, tz=local_tz)
            dt_str = dt_local.strftime(dt_format)

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