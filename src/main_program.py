"""Main program loop for the weather application."""

from dotenv import load_dotenv, find_dotenv
import os

from src.get_current_weather import get_weather_with_uv
from src.get_weather_forecast import get_forecast
from src.config_loader import load_config


def _validate_city_name(city: str, extra_chars: str) -> bool:
    """Check if city name contains only allowed characters.

    Letters (including Finnish å, ä, ö) are always allowed.
    Additional characters (hyphens, apostrophes, etc.) come from config.
    """
    allowed = set("abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ" + extra_chars)
    return bool(city) and set(city).issubset(allowed)


def run():
    """Entry point for the weather application."""
    print()
    print('Welcome to the weather app!')
    print('---------------------------')
    print()

    load_dotenv(find_dotenv())
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    # Validate API key
    if not api_key:
        print("Error: OpenWeatherMap API key not found!")
        print("Please set your API key in the .env file as:")
        print("OPENWEATHERMAP_API_KEY=your_api_key_here")
        print("\nYou can get a free API key from: https://openweathermap.org/api")
        return

    if not api_key.strip():
        print("Error: OpenWeatherMap API key is empty!")
        print("Please check your .env file and make sure the API key is properly set.")
        return

    config = load_config()
    display = config['display']
    extra_chars = config['input']['allowed_extra_chars']

    running = True
    city = None

    while running:
        output = ""

        # Get city name if not reusing
        if not city:
            while True:
                city = input('Enter a city (or type "exit" to quit): ').strip().lower()
                if city == "exit":
                    print('Thanks for using the app. Goodbye!')
                    return
                if _validate_city_name(city, extra_chars):
                    break
                print('Please enter a valid city name.\n')

        # Choose current weather or forecast
        while True:
            choice = input('Current weather or 3-day forecast? (1 = current, 2 = forecast): ')
            if choice in ('1', '2'):
                break
            print('Please enter 1 or 2.')

        if choice == '1':
            weather = get_weather_with_uv(api_key, city)
            if weather:
                print()
                print(f'Current weather in {city.capitalize()}:')
                for key, value in weather.items():
                    output += f'{key.capitalize()}: {value}\n'
            else:
                print(f"Sorry, weather data for {city.capitalize()} could not be retrieved.")
                if input('Try another city? (1 = yes, 2 = no): ') == '2':
                    print('Goodbye!')
                    return
                city = None
                continue

        else:
            forecasts = get_forecast(api_key, city)
            if forecasts:
                temp_unit = display['temperature_unit']
                wind_unit = display['wind_unit']
                print()
                print(f'3-day forecast for {city.capitalize()}:\n')
                for f in forecasts:
                    output += f"Date and Time: {f['datetime']}\n"
                    output += f"Temperature: {f['temperature']}{temp_unit}\n"
                    output += f"Description: {f['description']}\n"
                    output += f"Humidity: {f['humidity']}%\n"
                    output += f"Wind Speed: {f['wind_speed']} {wind_unit}\n"
                    output += f"UV Index: {f['uv_index']}\n"
                    output += '-----------------------------------\n'
            else:
                print(f"Sorry, forecast for {city.capitalize()} could not be retrieved.")
                if input('Try another city? (1 = yes, 2 = no): ') == '2':
                    print('Goodbye!')
                    return
                city = None
                continue

        print(output)

        # Next action
        while True:
            again = input('What next? (1 = new city, 2 = reuse same city, 3 = quit): ')
            if again == '3':
                print('Goodbye!\n')
                running = False
                break
            if again == '1':
                city = None
                break
            if again == '2':
                break
            print('Please enter 1, 2, or 3.')