import requests
from datetime import datetime
import pytz  # For timezone conversion in datetime

from src.get_uv_index import get_uv_index

def get_weather_with_uv(owm_api_key: str, city: str):  # Function to get weather from OpenWeatherMap API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={owm_api_key}&units=metric'

    try:
        response = requests.get(url).json()

        # Extract latitude and longitude from the weather response
        lat = response['coord']['lat']
        lon = response['coord']['lon']

        # Get the UV index using the latitude and longitude
        uv_response = get_uv_index(owm_api_key, lat, lon)

        # Convert sunrise and sunset time from unix timestamp to datetime
        sunrise_time = datetime.fromtimestamp(response['sys']['sunrise'], pytz.utc)
        sunset_time = datetime.fromtimestamp(response['sys']['sunset'], pytz.utc)

        # Prepare the weather dictionary with relevant data
        weather = {
            'city': response['name'],
            'temperature': response['main']['temp'],
            'feels_like': response['main']['feels_like'],
            'temp_max': response['main']['temp_max'],
            'temp_min': response['main']['temp_min'],
            'description': response['weather'][0]['description'],
            'humidity': response['main']['humidity'],
            'wind_speed': response['wind']['speed'],
            'wind_direction': response['wind']['deg'],
            'sunrise': sunrise_time.strftime("%Y-%m-%d %H:%M:%S"),
            'sunset': sunset_time.strftime("%Y-%m-%d %H:%M:%S"),
            'icon': response['weather'][0]['icon'],
            'uv_index': uv_response,
            'cloudiness': response['clouds']['all'],
            'pressure': response['main']['pressure'],
            'visibility': response.get('visibility', 'N/A'),
            'rain': response.get('rain', {}).get('1h', '0 mm'),
            'snow': response.get('snow', {}).get('1h', '0 mm')
        }

        return weather
    except Exception as e:
        print(f"Error: {e}")
        return None
