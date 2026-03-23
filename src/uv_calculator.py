"""Shared UV index estimation based on solar altitude angle."""

import math
from datetime import datetime
import pytz
from pysolar.solar import get_altitude


def estimate_uv_index(lat: float, lon: float, dt_utc: datetime, uv_peak: float) -> float:
    """Estimate UV index from solar position.

    Uses the sun's altitude angle to scale a peak UV value.
    This is an approximation — real UV depends on cloud cover,
    ozone layer thickness, and surface reflection.

    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        dt_utc: UTC datetime for the calculation.
        uv_peak: Estimated maximum UV index for the location.

    Returns:
        Estimated UV index (0.0 if sun is below horizon).
    """
    altitude_deg = get_altitude(lat, lon, dt_utc)

    if altitude_deg > 0:
        return round(uv_peak * math.sin(math.radians(altitude_deg)), 2)

    return 0.0