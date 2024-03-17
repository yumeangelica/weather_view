from dotenv import load_dotenv, find_dotenv
import os

from src.get_current_weather import get_weather_with_uv
from src.get_weather_forecast import get_forecast

def run():
    print('Welcome to the weather app!')
    print('---------------------------')

    load_dotenv(find_dotenv()) # Loads environment variables from .env file
    api_key = os.getenv('API_KEY') # Gets API key from .env file

    allowed_characters = set("abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ ")

    run = True # Boolean to keep the program running

    while run:
        output = "" # Output string to be printed, resets on every iteration


        # Ask user for a city, and validate input
        while True:
            city = input('Enter a city: ').lower()

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
                break  # Breaks out of the loop if a valid input is received
            except ValueError:
                print('Please enter a valid number.')


        # If user wants the current weather, get the current weather
        if current_or_forecast == 1:
            weather = get_weather_with_uv(api_key, city) # Gets response from API as a dictionary

            print()
            print(f'Current weather in {city.capitalize()}:')


            if (weather != None):

                for key, value in weather.items():
                    match key:
                        case 'temperature':
                            output += f'{key}: {value}°C\n'
                        case 'feels_like':
                            output += f'{key}: {value}°C\n'
                        case 'wind_direction':
                            match value:
                                case 0:
                                    output += f'{key}: North\n'
                                case 90:
                                    output += f'{key}: East\n'
                                case 180:
                                    output += f'{key}: South\n',
                                case 270:
                                    output += f'{key}: West\n'
                                case _ if value > 0 and value < 90:
                                    output += f'{key}: North-East\n'
                                case _ if value > 90 and value < 180:
                                    output += f'{key}: South-East\n'
                                case _ if value > 180 and value < 270:
                                    output += f'{key}: South-West\n'
                                case _ if value > 270 and value < 360:
                                    output += f'{key}: North-West\n'
                        case 'sunrise', 'sunset':
                            output += f'{key}: {value}\n'
                        case 'uv_index':
                            output += f'{key}: {value}\n'
                        case 'cloudiness':
                            output += f"Cloudiness: {value}%\n"
                        case 'pressure':
                            output += f"Pressure: {value} hPa\n"
                        case 'visibility':
                            output += f"Visibility: {int(value)/1000} km\n"  # Convert to km
                        case 'rain' | 'snow':
                            output += f"{key.capitalize()} (last 1 hr): {value}\n"  # Using value from dictionary
                        case _:
                            output += f'{key}: {value}\n'
            else:
                print('Sorry, the city you entered is not found.')
                print('---------------------------')
                continue


        # If user wants the forecast, get the forecast
        if current_or_forecast == 2:
            forecasts = get_forecast(api_key, city) # Gets response from API as a list of dictionaries

            if forecasts is not None:
                print()
                print(f'3-day forecast for {city.capitalize()}:\n')

                for forecast in forecasts:
                    output += f"Date and Time: {forecast['datetime']}\n"
                    output += f"Temperature: {forecast['temperature']}°C\n"
                    output += f"Description: {forecast['description']}\n"
                    output += f"Humidity: {forecast['humidity']}%\n"
                    output += f"Wind Speed: {forecast['wind_speed']} m/s\n"
                    output += f"UV Index: {forecast['uv_index']}\n"
                    output += '-----------------------------------\n'
            else:
                print('Sorry, the forecast for the city you entered is not found.')
                print('---------------------------')
                continue

        print(output)


        # Ask user if they want to enter a new city, and validate input
        while True:
            again = input('New city? (y/n): ')
            if again == 'n':
                print('Thanks for using the app. Good bye!')
                print()
                run = False
                break
            elif again == 'y':
                break
            else:
                print('Please enter y or n.')
                continue




