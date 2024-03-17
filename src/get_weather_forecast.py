from datetime import datetime
import requests
import pytz # For timezone conversion in datetime

from src.get_uv_index import get_uv_index

def get_forecast(api_key: str, city: str):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=24'

    try:
        response = requests.get(url).json()
        forecasts = []

        # Extract lat and lon from the weather response
        lat = response['city']['coord']['lat']
        lon = response['city']['coord']['lon']

        # Get the UV index using the latitude and longitude for first day morning
        uv_response = get_uv_index(api_key, lat, lon)

        for item in response['list']:
            # Change unix timestamp to datetime
            dt = datetime.fromtimestamp(item['dt'], pytz.utc)
            forecast = {
                'datetime': dt.strftime("%Y-%m-%d %H:%M:%S"),
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'icon': item['weather'][0]['icon'],
                'uv_index': uv_response if item == response['list'][0] else 'N/A' # UV index is only available for the first day morning
            }
            forecasts.append(forecast)
        return forecasts
    except:
        return None


