from dotenv import load_dotenv, find_dotenv
import os

from src.get_current_weather import get_weather_with_uv
from src.get_weather_forecast import get_forecast

def run():
    print()
    print('Welcome to the weather app!')
    print('---------------------------')
    print()

    load_dotenv(find_dotenv())  # Load environment variables from .env file
    owm_api_key = os.getenv('OMW_API_KEY')  # OpenWeatherMap API key
    uv_api_key = os.getenv('UV_API_KEY')  # WeatherAPI.com API key

    allowed_characters = set("abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ ")

    run = True  # Keep the program running
    city = None  # Initialize city to None

    while run:
        output = ""  # Reset the output string on each iteration

        # Ask user for a city and validate input if city is None or user wants to change the city
        if not city:
            while True:
                city = input('Enter a city (or type "exit" to quit): ').lower()

                if city == "exit":
                    print('Thanks for using the app. Goodbye!')
                    return  # Exit the function and terminate the program

                if set(city).issubset(allowed_characters):
                    break
                else:
                    print('Please enter a valid city name.\n')

        # Ask user if they want the current weather or the forecast, and validate input
        while True:
            try:
                current_or_forecast = int(input('Do you want the current weather or the 3-day forecast? (1 = current, 2 = forecast): '))
                if current_or_forecast not in [1, 2]:
                    print('Please enter 1 or 2.')
                    continue
                break  # Exit the loop if a valid input is received
            except ValueError:
                print('Please enter a valid number.')

        # If the user wants the current weather
        if current_or_forecast == 1:
            weather = get_weather_with_uv(owm_api_key, city)  # Get the weather from OpenWeatherMap

            if weather is not None:
                print()
                print(f'Current weather in {city.capitalize()}:')
                for key, value in weather.items():
                    output += f'{key.capitalize()}: {value}\n'
            else:
                print(f'Sorry, the weather data for {city.capitalize()} could not be retrieved.')
                continue_option = input('Would you like to try another city? (1 = yes, 2 = no): ').lower()
                if continue_option == '2':
                    print('Thanks for using the app. Goodbye!')
                    return  # Exit the function and terminate the program
                else:
                    city = None  # Reset city to allow user to enter a new city
                    continue  # Prompt the user to enter a new city

        # If the user wants the forecast
        if current_or_forecast == 2:
            forecasts = get_forecast(owm_api_key, uv_api_key, city)  # Get the forecast and UV index

            if forecasts is not None:
                print()
                print(f'3-day forecast for {city.capitalize()}:\n')
                for forecast in forecasts:
                    if forecast['uv_index'] != 'N/A':
                        output += f"Date and Time: {forecast['datetime']}\n"
                        output += f"Temperature: {forecast['temperature']}°C\n"
                        output += f"Description: {forecast['description']}\n"
                        output += f"Humidity: {forecast['humidity']}%\n"
                        output += f"Wind Speed: {forecast['wind_speed']} m/s\n"
                        output += f"UV Index: {forecast['uv_index']}\n"
                        output += '-----------------------------------\n'
            else:
                print(f'Sorry, the forecast data for {city.capitalize()} could not be retrieved.')
                continue_option = input('Would you like to try another city? (1 = yes, 2 = no): ').lower()
                if continue_option == '2':
                    print('Thanks for using the app. Goodbye!\n')
                    return  # Exit the function and terminate the program
                else:
                    city = None  # Reset city to allow user to enter a new city
                    continue  # Prompt the user to enter a new city

        print(output)

        # Ask user if they want to enter a new city, reuse the same city, or quit
        while True:
            again = input('What would you like to do next? (1 = new city, 2 = reuse same city, 3 = quit): ').lower()
            if again == '3':
                print('Thanks for using the app. Goodbye!\n')
                run = False
                break
            elif again == '1':
                city = None  # Reset city to allow user to enter a new city
                break
            elif again == '2':
                break
            else:
                print('Please enter 1, 2, or 3.')
                continue
