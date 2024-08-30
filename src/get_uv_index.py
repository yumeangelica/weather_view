import requests

def get_uv_index(owm_api_key: str, lat: float, lon: float):
    url = f'http://api.openweathermap.org/data/2.5/uvi?appid={owm_api_key}&lat={lat}&lon={lon}'
    response = requests.get(url).json()
    return response['value']  # Returns the UV index value from the response
