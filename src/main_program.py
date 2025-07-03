from dotenv import load_dotenv, find_dotenv
import os

from src.get_current_weather import get_weather_with_uv
from src.get_weather_forecast import get_forecast

def run():
    print()
    print('Welcome to the weather app!')
    print('---------------------------')
    print()

    load_dotenv(find_dotenv())
    openweathermap_api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    # Check if API key is set
    if not openweathermap_api_key:
        print("Error: OpenWeatherMap API key not found!")
        print("Please set your API key in the .env file as:")
        print("OPENWEATHERMAP_API_KEY=your_api_key_here")
        print("\nYou can get a free API key from: https://openweathermap.org/api")
        return

    if not openweathermap_api_key.strip():
        print("Error: OpenWeatherMap API key is empty!")
        print("Please check your .env file and make sure the API key is properly set.")
        return

    allowed_characters = set("abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ ")

    running = True
    city = None

    while running:
        output = ""

        if not city:
            while True:
                city = input('Enter a city (or type "exit" to quit): ').strip().lower()
                if city == "exit":
                    print('Thanks for using the app. Goodbye!')
                    return
                if set(city).issubset(allowed_characters):
                    break
                print('Please enter a valid city name.\n')

        while True:
            choice = input('Do you want the current weather or the 3-day forecast? (1 = current, 2 = forecast): ')
            if choice in ('1', '2'):
                current_or_forecast = int(choice)
                break
            print('Please enter 1 or 2.')

        if current_or_forecast == 1:
            weather = get_weather_with_uv(openweathermap_api_key, city) # type: ignore
            if weather:
                print()
                print(f'Current weather in {city.capitalize()}:')
                for key, value in weather.items():
                    output += f'{key.capitalize()}: {value}\n'
            else:
                print(f"Sorry, the weather data for {city.capitalize()} could not be retrieved.")
                if input('Try another city? (1 = yes, 2 = no): ') == '2':
                    print('Goodbye!')
                    return
                city = None
                continue

        else:
            forecasts = get_forecast(openweathermap_api_key, city) # type: ignore
            if forecasts:
                print()
                print(f'3-day forecast for {city.capitalize()}:\n')
                for f in forecasts:
                    output += f"Date and Time: {f['datetime']}\n"
                    output += f"Temperature: {f['temperature']}°C\n"
                    output += f"Description: {f['description']}\n"
                    output += f"Humidity: {f['humidity']}%\n"
                    output += f"Wind Speed: {f['wind_speed']} m/s\n"
                    output += f"UV Index: {f['uv_index']}\n"
                    output += '-----------------------------------\n'
            else:
                print(f"Sorry, the forecast for {city.capitalize()} could not be retrieved.")
                if input('Try another city? (1 = yes, 2 = no): ') == '2':
                    print('Goodbye!')
                    return
                city = None
                continue

        print(output)

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
