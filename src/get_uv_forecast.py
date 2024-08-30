from requests import get

def get_uv_forecast(location: str, uv_api_key: str):
    url = f'http://api.weatherapi.com/v1/forecast.json'

    params = {
        'key': uv_api_key,  # Use the UV API key from WeatherAPI.com
        'q': location,
        'days': 3,
        'aqi': 'no',
        'alerts': 'no',
    }

    response = get(url, params=params)
    data = response.json()

    if 'error' in data:
        return None

    forecast = []

    for day in data['forecast']['forecastday']:
        uv = day['day']['uv']
        date = day['date']
        forecast.append({'date': date, 'uv': uv})

    return forecast
