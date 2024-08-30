# Weather View Application

## Overview
This is a Python-based application designed to provide real-time weather information for any specified city. Utilizing the OpenWeatherMap API, it displays current weather details such as temperature, weather conditions, humidity, UV index, and more. Additionally, the application now supports a 3-day UV index forecast, retrieved using the WeatherAPI.com service. This user-friendly application can be tailored for various global locations.

## Features
- Fetches and displays current weather data including temperature, weather description, humidity, UV index, etc.
- Provides a 3-day weather and UV index forecast.
- Easy to use with command line arguments for city selection.
- Real-time data retrieval from OpenWeatherMap API and WeatherAPI.com for UV forecasts.

## Prerequisites
- Python 3.12.0
- pip 23.2.1

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
3. Setup your `.env` file in the root directory. Add your OpenWeatherMap and WeatherAPI.com API keys in this format:
   ```plaintext
   OMW_API_KEY=your_openweathermap_api_key
   UV_API_KEY=your_weatherapi_api_key
    ```

## Installing dependencies
1. Navigate to the project's root directory.
2. Run the following command to install all required dependencies:
```bash
pip3 install -r requirements.txt
```

## Running the application
1. Navigate to the project's root directory.
2. Run the following command to execute the application:
```bash
python3 main.py
```

## Usage
After starting the application, you will be prompted for the following inputs:
1. **City Name**: Enter the name of the city for which you want to fetch weather data.
2. **Data Choice**: Enter `1` to fetch the current weather or `2` for the 3-day forecast.
3. **Next Step**: After displaying the data, choose whether to enter a new city, reuse the same city for different data, or quit.


## Credits
This project was developed by yumeangelica. For more information on how this work can be used, please refer to the LICENSE.txt file.

Copyright © 2024 - present; yumeangelica


## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. For more information, see the LICENSE file in this repository.
