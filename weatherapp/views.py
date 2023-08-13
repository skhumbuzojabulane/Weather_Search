import os
import requests
import re
from datetime import datetime, timedelta
from django.shortcuts import render
from decouple import config

def sanitize_filename(filename):
    # Remove characters that are not suitable for filenames
    sanitized = re.sub(r'[^\w\s-]', '', filename)
    return sanitized

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15)  # Convert and round to the nearest whole number

def weather_search(request):
    city_name = request.GET.get('city')
    weather_data = None

    if city_name:
        geocoding_api_key = config('GEOCODING_API_KEY')
        geocoding_url = f"http://api.positionstack.com/v1/forward?access_key={geocoding_api_key}&query={city_name}"

        geocoding_response = requests.get(geocoding_url)
        geocoding_data = geocoding_response.json()

        if geocoding_data and 'data' in geocoding_data and len(geocoding_data['data']) > 0:
            latitude = geocoding_data['data'][0]['latitude']
            longitude = geocoding_data['data'][0]['longitude']

            # Construct cache file path
            filename = f"{geocoding_data['data'][0]['label']}_{latitude}_{longitude}.txt"
            sanitized_filename = sanitize_filename(filename)
            file_path = os.path.join('weather_cache', sanitized_filename)

            if os.path.exists(file_path):
                # Get the file modification timestamp
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Check if the cache is older than 180 minutes (3 hours)
                if datetime.now() - file_mod_time > timedelta(minutes=180):
                    # Fetch and update data from OpenWeatherMap
                    weather_api_key = config('WEATHER_API_KEY')
                    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api_key}"
                    current_weather_response = requests.get(current_weather_url)
                    current_weather_data = current_weather_response.json()

                    # Save updated data to the cache file
                    with open(file_path, 'w') as file:
                        file.write(str(current_weather_data))
                        file.write('\n')

                # Read data from cache file
                with open(file_path, 'r') as file:
                    cached_weather_data = file.read()
                    weather_data = eval(cached_weather_data)  # Convert string back to dictionary

            else:
                # Fetch weather data using latitude and longitude
                weather_api_key = config('WEATHER_API_KEY')
                current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api_key}"
                current_weather_response = requests.get(current_weather_url)
                current_weather_data = current_weather_response.json()

                # Save data to the cache file
                with open(file_path, 'w') as file:
                    file.write(str(current_weather_data))
                    file.write('\n')

                # Convert temperature from Kelvin to Celsius
                current_weather_data['main']['temp'] = f"{kelvin_to_celsius(current_weather_data['main']['temp'])}°C"
                weather_data = current_weather_data  # Display current weather in template

    return render(request, 'weatherapp/weather_search.html', {'weather_data': weather_data})
