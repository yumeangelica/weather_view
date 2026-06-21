# Weather View

A small Python command-line app for checking current weather and 3-day forecasts with the [OpenWeatherMap API](https://openweathermap.org/api). It also estimates UV index values from solar altitude using `pysolar`.

## Features

- Current weather: temperature, humidity, wind, pressure, sunrise/sunset, cloudiness, rain, and snow
- 3-day forecast in 3-hour intervals with estimated UV index values
- Config-driven API settings, display formats, UV peak value, and city input rules
- Timezone-aware timestamps based on the queried city's local offset
- Clear handling for missing API keys, API errors, timeouts, connection failures, and malformed responses
- Focused unit tests for validation, configuration loading, UV estimation, and API client behavior

## Project Structure

```text
weather_view/
├── main.py
├── requirements.txt
├── config/
│   └── weather_config.json
├── src/
│   ├── config_loader.py
│   ├── get_current_weather.py
│   ├── get_weather_forecast.py
│   ├── main_program.py
│   └── uv_calculator.py
└── tests/
    ├── test_config_loader.py
    ├── test_main_program.py
    ├── test_uv_calculator.py
    └── test_weather_clients.py
```

## Requirements

- Python 3.10+
- An OpenWeatherMap API key

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```text
OPENWEATHERMAP_API_KEY=your_api_key_here
```

You can create a free API key from [OpenWeatherMap](https://openweathermap.org/api). The `.env` file is ignored by Git and should not be committed.

## Usage

```bash
python3 main.py
```

The app will ask for:

1. City name, for example `helsinki`, `london`, or `new york`. Type `exit` to quit.
2. Data type: `1` for current weather or `2` for 3-day forecast.
3. Next action: `1` for a new city, `2` to reuse the same city, or `3` to quit.

## Configuration

Runtime settings live in `config/weather_config.json`:

- OpenWeatherMap endpoints, timeout, units, and forecast count
- Display units and datetime format
- Estimated peak UV value
- Extra characters allowed in city names

If the config file is missing or invalid, the app falls back to built-in defaults and prints a warning.

## Testing

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

You can also run a quick syntax check:

```bash
python -m compileall -q main.py src tests
```

## UV Index Note

The UV index is estimated from solar altitude, not fetched from a dedicated UV API. It uses a configurable peak UV value scaled by `sin(solar_altitude)`, so actual UV conditions may differ because of clouds, ozone, altitude, and surface reflection. Nighttime values return `0.0`.

## Troubleshooting

- **"API key not found"**: make sure `.env` exists in the project root and contains `OPENWEATHERMAP_API_KEY`.
- **"API error"**: verify that your OpenWeatherMap API key is valid and active.
- **"Request timed out"**: the weather service may be temporarily unavailable, or the timeout may need adjustment in `weather_config.json`.
- **"Unexpected response format"**: the API returned data in a format the app could not parse.
- **UV index is always 0**: this is expected during nighttime in the queried city.
- **City not found**: try the full city name or check the spelling.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

Copyright © 2024 – present, [yumeangelica](https://github.com/yumeangelica)
