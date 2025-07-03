# Weather View Application

## Overview

This is a Python-based application designed to provide real-time weather information for any specified city. Utilizing the OpenWeatherMap API, it displays current weather details such as temperature, weather conditions, humidity, UV index, and more. Additionally, the application supports a 3-day weather forecast with UV index calculations using the pysolar library for solar position calculations. This user-friendly application can be tailored for various global locations.

## Features

- Fetches and displays current weather data including temperature, weather description, humidity, UV index, etc.
- Provides a 3-day weather forecast with UV index calculations using solar position algorithms.
- Easy to use with interactive command line interface for city selection.
- Real-time data retrieval from OpenWeatherMap API.
- UV index calculation using pysolar library for accurate solar position calculations.
- Input validation for city names and API key verification.
- Proper timezone handling for accurate local times.

## Prerequisites

- Python 3.8+ (tested with Python 3.12)
- pip (latest version recommended)

## Installation

### Python and pip

Ensure you have the correct versions of Python and pip installed. Download Python [here](https://www.python.org/downloads/) which includes pip.

To check your Python version:

```bash
python3 --version
```

To check your pip version:

```bash
pip3 --version
```

## Setting up the project:

1. Clone the repository.
2. Navigate to the project's root directory.
3. Setup your `.env` file in the root directory. Add your OpenWeatherMap API key in this format:
   ```plaintext
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   ```

**Note**: The application will check if your API key is properly set before starting. If the API key is missing or invalid, you'll receive clear instructions on how to fix it.

You can get a free API key from [OpenWeatherMap](https://openweathermap.org/api).

## Installing dependencies

1. Navigate to the project's root directory.
2. Run the following command to install all required dependencies:

```bash
pip3 install -r requirements.txt
```

### Dependencies included:

- `python-dotenv`: For loading environment variables from .env file
- `requests`: For making HTTP API requests to OpenWeatherMap
- `pytz`: For timezone handling and local time calculations
- `pysolar`: For solar position calculations used in UV index computation

## Running the application

1. Navigate to the project's root directory.
2. Run the following command to execute the application:

```bash
python3 main.py
```

## Usage

After starting the application, you will be prompted for the following inputs:

1. **City Name**: Enter the name of the city for which you want to fetch weather data (or type "exit" to quit).
2. **Data Choice**: Enter `1` to fetch the current weather or `2` for the 3-day forecast.
3. **Next Step**: After displaying the data, choose whether to:
   - Enter `1` for a new city
   - Enter `2` to reuse the same city for different data
   - Enter `3` to quit the application

The application includes input validation to ensure city names contain only valid characters and will prompt you to re-enter if invalid input is provided.

## Troubleshooting

### Common Issues:

1. **"API key not found" error**: Make sure your `.env` file is in the project root directory and contains the correct API key format.
2. **"API error" messages**: Check that your OpenWeatherMap API key is valid and active.
3. **UV index shows 0**: This is normal during nighttime hours in the selected city.
4. **City not found**: Try using the full city name or check the spelling.

## Credits

This project was developed by yumeangelica. For more information on how this work can be used, please refer to the LICENSE.txt file.

Copyright © 2024 - present; yumeangelica

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more information, see the LICENSE file in this repository.
