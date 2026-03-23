# Weather View

## Overview

A Python application that fetches real-time weather data and 3-day forecasts for any city using the [OpenWeatherMap API](https://openweathermap.org/api). Includes estimated UV index calculations based on solar position via the pysolar library.

## Features

- Current weather: temperature, humidity, wind, pressure, sunrise/sunset, cloudiness, rain/snow
- 3-day forecast in 3-hour intervals with UV index estimation
- Config-driven settings — API parameters, UV peak value, display formats, and input rules live in a JSON file
- Shared UV calculator module to avoid code duplication
- Proper error handling with specific messages for timeouts, connection failures, and unexpected responses
- Input validation for city names (configurable allowed characters)
- Timezone-aware timestamps using the city's local time

## Project Structure

\```
weather_view/
├── main.py                          # Entry point
├── requirements.txt
├── .env                             # API key (not committed)
├── config/
│   └── weather_config.json          # API URLs, UV settings, display formats
└── src/
    ├── __init__.py
    ├── main_program.py              # CLI input loop
    ├── get_current_weather.py       # Current weather fetcher
    ├── get_weather_forecast.py      # Forecast fetcher
    ├── uv_calculator.py             # Shared UV index estimation
    └── config_loader.py             # Config file loader with caching
\```

## Prerequisites

- Python 3.10+
- pip

## Installation

1. Clone the repository:
\```bash
git clone <repository-url>
cd weather_view
\```

2. Create a virtual environment and activate it:
\```bash
python3 -m venv venv
source venv/bin/activate
\```

3. Install dependencies:
\```bash
pip install -r requirements.txt
\```

4. Create a `.env` file in the project root with your API key:
\```
OPENWEATHERMAP_API_KEY=your_api_key_here
\```

You can get a free API key from [OpenWeatherMap](https://openweathermap.org/api).

## Configuration

### API Key (`.env`)

The API key is loaded from a `.env` file via python-dotenv. The app validates the key on startup and provides clear instructions if it's missing or empty.

### App Settings (`config/weather_config.json`)

Controls API endpoints, request timeout, units, UV estimation peak value, display formats, and allowed characters in city name input. All settings have sensible defaults built into the code as a fallback.

## Usage

\```bash
python3 main.py
\```

You will be prompted for:

1. **City name** — e.g. `helsinki`, `london`, `new york`. Type `exit` to quit.
2. **Data type** — `1` for current weather, `2` for 3-day forecast.
3. **Next action** — `1` for new city, `2` to reuse same city, `3` to quit.

## UV Index Note

The UV index is estimated using solar altitude angle calculations (via pysolar), not from a dedicated UV API. The estimation uses a configurable peak UV value (default: 8.0) scaled by `sin(solar_altitude)`. This is an approximation — actual UV depends on cloud cover, ozone, and surface conditions. The UV index will show 0.0 during nighttime hours.

## Troubleshooting

- **"API key not found"** — make sure `.env` exists in the project root with the correct format.
- **"API error"** — verify your API key is valid and active at openweathermap.org.
- **"Request timed out"** — the weather service may be temporarily unavailable. The timeout is configurable in `weather_config.json`.
- **UV index is always 0** — normal during nighttime in the queried city.
- **City not found** — try the full city name or check spelling.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

Copyright © 2024 – present, [yumeangelica](https://github.com/yumeangelica)