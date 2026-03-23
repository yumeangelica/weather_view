"""Config loader for the weather application."""

import json
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_config_cache = None


def load_config() -> dict:
    """Load weather_config.json with caching.

    Returns:
        Config dictionary. Falls back to sensible defaults if file is missing.
    """
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    config_path = os.path.join(_project_root, 'config', 'weather_config.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            _config_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Warning: Could not load config ({e}). Using defaults.")
        _config_cache = {
            "api": {
                "base_url": "https://api.openweathermap.org/data/2.5",
                "current_endpoint": "/weather",
                "forecast_endpoint": "/forecast",
                "timeout": 10,
                "units": "metric",
                "forecast_count": 24
            },
            "uv": {"peak_value": 8.0},
            "display": {
                "datetime_format": "%Y-%m-%d %H:%M:%S %Z",
                "temperature_unit": "°C",
                "wind_unit": "m/s"
            },
            "input": {"allowed_extra_chars": "-'. "}
        }

    return _config_cache