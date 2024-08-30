from datetime import datetime
import requests
import pytz  # For timezone conversion in datetime
from src.get_uv_forecast import get_uv_forecast  # Import UV forecast function

def get_forecast(owm_api_key: str, uv_api_key: str, city: str):
    # OpenWeatherMap forecast URL
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={owm_api_key}&units=metric&cnt=24'

    try:
        # Get the weather forecast from OpenWeatherMap
        response = requests.get(url).json()
        forecasts = []

        # Get the UV forecast from WeatherAPI.com
        uv_forecast = get_uv_forecast(city, uv_api_key)

        if uv_forecast is None:
            return None  # Handle the error if the UV forecast could not be retrieved

        # Map UV index by date
        uv_index_by_date = {entry['date']: entry['uv'] for entry in uv_forecast}

        for item in response['list']:
            # Convert unix timestamp to datetime
            dt = datetime.fromtimestamp(item['dt'], pytz.utc)
            date_str = dt.strftime("%Y-%m-%d")

            forecast = {
                'datetime': dt.strftime("%Y-%m-%d %H:%M:%S"),
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'icon': item['weather'][0]['icon'],
                'uv_index': uv_index_by_date.get(date_str, 'N/A')  # Link UV index to the correct date
            }
            forecasts.append(forecast)
        return forecasts
    except Exception as e:
        print(f"Error: {e}")
        return None
