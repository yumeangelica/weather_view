"""Tests for OpenWeatherMap API client modules."""

import unittest
from unittest.mock import patch

from src.get_current_weather import get_weather_with_uv
from src.get_weather_forecast import get_forecast


TEST_CONFIG = {
    "api": {
        "base_url": "https://api.example.test",
        "current_endpoint": "/weather",
        "forecast_endpoint": "/forecast",
        "timeout": 3,
        "units": "metric",
        "forecast_count": 2,
    },
    "uv": {"peak_value": 8.0},
    "display": {
        "datetime_format": "%Y-%m-%d %H:%M:%S %Z",
        "temperature_unit": "C",
        "wind_unit": "m/s",
    },
    "input": {"allowed_extra_chars": "-'. "},
}


class MockResponse:
    def __init__(self, status_code, payload=None, json_error=None):
        self.status_code = status_code
        self.payload = payload
        self.json_error = json_error

    def json(self):
        if self.json_error:
            raise self.json_error

        return self.payload


class CurrentWeatherClientTest(unittest.TestCase):
    def test_returns_current_weather_with_estimated_uv(self):
        payload = {
            "coord": {"lat": 60.17, "lon": 24.94},
            "timezone": 7200,
            "sys": {"sunrise": 1781671200, "sunset": 1781730000},
            "name": "Helsinki",
            "main": {
                "temp": 18.5,
                "feels_like": 17.9,
                "temp_max": 19.0,
                "temp_min": 17.0,
                "humidity": 64,
                "pressure": 1014,
            },
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 4.2, "deg": 220},
            "clouds": {"all": 12},
            "visibility": 10000,
        }
        response = MockResponse(200, payload)

        with patch("src.get_current_weather.load_config", return_value=TEST_CONFIG):
            with patch("src.get_current_weather.estimate_uv_index", return_value=4.2):
                with patch("src.get_current_weather.requests.get", return_value=response) as get:
                    result = get_weather_with_uv("api-key", "helsinki")

        self.assertEqual(result["city"], "Helsinki")
        self.assertEqual(result["uv_index"], 4.2)
        self.assertEqual(result["rain"], "0 mm")
        get.assert_called_once_with(
            "https://api.example.test/weather",
            params={"q": "helsinki", "appid": "api-key", "units": "metric"},
            timeout=3,
        )

    def test_returns_none_for_invalid_json(self):
        response = MockResponse(200, json_error=ValueError("bad json"))

        with patch("src.get_current_weather.load_config", return_value=TEST_CONFIG):
            with patch("src.get_current_weather.requests.get", return_value=response):
                with patch("builtins.print") as print_mock:
                    result = get_weather_with_uv("api-key", "helsinki")

        self.assertIsNone(result)
        print_mock.assert_called_once()
        self.assertIn("invalid JSON", print_mock.call_args.args[0])


class ForecastClientTest(unittest.TestCase):
    def test_returns_forecast_with_estimated_uv(self):
        payload = {
            "city": {
                "coord": {"lat": 60.17, "lon": 24.94},
                "timezone": 7200,
            },
            "list": [
                {
                    "dt": 1781690400,
                    "main": {"temp": 19.0, "humidity": 58},
                    "weather": [{"description": "few clouds", "icon": "02d"}],
                    "wind": {"speed": 3.6},
                }
            ],
        }
        response = MockResponse(200, payload)

        with patch("src.get_weather_forecast.load_config", return_value=TEST_CONFIG):
            with patch("src.get_weather_forecast.estimate_uv_index", return_value=5.1):
                with patch("src.get_weather_forecast.requests.get", return_value=response) as get:
                    result = get_forecast("api-key", "helsinki")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["temperature"], 19.0)
        self.assertEqual(result[0]["uv_index"], 5.1)
        get.assert_called_once_with(
            "https://api.example.test/forecast",
            params={
                "q": "helsinki",
                "appid": "api-key",
                "units": "metric",
                "cnt": 2,
            },
            timeout=3,
        )

    def test_returns_none_for_invalid_json(self):
        response = MockResponse(200, json_error=ValueError("bad json"))

        with patch("src.get_weather_forecast.load_config", return_value=TEST_CONFIG):
            with patch("src.get_weather_forecast.requests.get", return_value=response):
                with patch("builtins.print") as print_mock:
                    result = get_forecast("api-key", "helsinki")

        self.assertIsNone(result)
        print_mock.assert_called_once()
        self.assertIn("invalid JSON", print_mock.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
