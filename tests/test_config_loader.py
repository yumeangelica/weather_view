"""Tests for configuration loading."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src import config_loader


class LoadConfigTest(unittest.TestCase):
    def tearDown(self):
        config_loader._config_cache = None

    def test_uses_defaults_when_config_file_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_loader._config_cache = None

            with patch.object(config_loader, "_project_root", temp_dir):
                with patch("builtins.print"):
                    config = config_loader.load_config()

        self.assertEqual(config["api"]["base_url"], "https://api.openweathermap.org/data/2.5")
        self.assertEqual(config["api"]["forecast_count"], 24)
        self.assertEqual(config["uv"]["peak_value"], 8.0)

    def test_caches_loaded_config(self):
        custom_config = {
            "api": {
                "base_url": "https://example.test",
                "current_endpoint": "/weather",
                "forecast_endpoint": "/forecast",
                "timeout": 5,
                "units": "metric",
                "forecast_count": 8,
            },
            "uv": {"peak_value": 6.0},
            "display": {
                "datetime_format": "%Y-%m-%d",
                "temperature_unit": "C",
                "wind_unit": "m/s",
            },
            "input": {"allowed_extra_chars": "-"},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config"
            config_dir.mkdir()
            config_path = config_dir / "weather_config.json"
            config_path.write_text(json.dumps(custom_config), encoding="utf-8")
            config_loader._config_cache = None

            with patch.object(config_loader, "_project_root", temp_dir):
                first = config_loader.load_config()
                config_path.write_text("{invalid json", encoding="utf-8")
                second = config_loader.load_config()

        self.assertIs(first, second)
        self.assertEqual(second["api"]["base_url"], "https://example.test")


if __name__ == "__main__":
    unittest.main()
