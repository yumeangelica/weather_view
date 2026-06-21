"""Tests for UV index estimation."""

from datetime import datetime
import unittest
from unittest.mock import patch

import pytz

from src.uv_calculator import estimate_uv_index


class EstimateUvIndexTest(unittest.TestCase):
    def test_scales_peak_value_by_solar_altitude(self):
        dt_utc = datetime(2026, 6, 17, 12, 0, tzinfo=pytz.utc)

        with patch("src.uv_calculator.get_altitude", return_value=30):
            result = estimate_uv_index(60.17, 24.94, dt_utc, 8.0)

        self.assertEqual(result, 4.0)

    def test_returns_zero_when_sun_is_below_horizon(self):
        dt_utc = datetime(2026, 6, 17, 0, 0, tzinfo=pytz.utc)

        with patch("src.uv_calculator.get_altitude", return_value=-5):
            result = estimate_uv_index(60.17, 24.94, dt_utc, 8.0)

        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()
