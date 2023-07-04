import requests
import json
from datetime import datetime, timedelta
import geocoder
from SecondaryFunctions import Functions as Sf

class WeatherPredictions():

    def week_weather(coordinates: list) -> tuple[str, list, list, list, list, list]:
        first_day = datetime.strftime(datetime.now() + timedelta(1), "%Y-%m-%d")
        last_day = datetime.strftime(datetime.now() + timedelta(7), "%Y-%m-%d")
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&daily=weathercode,temperature_2m_max,precipitation_probability_max,windspeed_10m_max&start_date={first_day}&end_date={last_day}&timezone=auto')
        response_json = response.json()
        place = Sf.place_name(coordinates[0], coordinates[1])
        weather_data = response_json.get('daily')
        time = weather_data.get('time')
        weather_code = weather_data.get('weathercode')
        temperature = weather_data.get('temperature_2m_max')
        precipitation_probability = weather_data.get('precipitation_probability_max')
        windspeed = weather_data.get('windspeed_10m_max')
        return place,time,weather_code,temperature,precipitation_probability,windspeed

    def two_week_weather(coordinates: list) -> tuple[str, list, list, list, list, list]:
        first_day = datetime.strftime(datetime.now() + timedelta(1), "%Y-%m-%d")
        last_day = datetime.strftime(datetime.now() + timedelta(14), "%Y-%m-%d")
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&daily=weathercode,temperature_2m_max,precipitation_probability_max,windspeed_10m_max&start_date={first_day}&end_date={last_day}&timezone=auto')
        response_json = response.json()
        place = Sf.place_name(coordinates[0], coordinates[1])
        weather_data = response_json.get('daily')
        time = weather_data.get('time')
        weather_code = weather_data.get('weathercode')
        temperature = weather_data.get('temperature_2m_max')
        precipitation_probability = weather_data.get('precipitation_probability_max')
        windspeed = weather_data.get('windspeed_10m_max')
        return place,time,weather_code,temperature,precipitation_probability,windspeed

    def hourly_weather(coordinates: list) -> tuple[str, list, list, list, list, list]:
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=temperature_2m,precipitation_probability,weathercode,windspeed_10m&models=best_match&forecast_days=2&timezone=auto')
        response_json = response.json()
        place = Sf.place_name(coordinates[0], coordinates[1])
        current_time = datetime.now()
        current_hour = current_time.hour
        weather_data = response_json.get('hourly')
        time, weather_code, temperature, precipitation_probability, windspeed  = [],[],[],[],[]
        for i in range(48):
            if current_hour == int(Sf.converter_date_into_hour(response_json.get('hourly').get('time')[i])):
                index = i
                break
        for i in range(index,index+12):
            time.append(weather_data.get('time')[i])
            weather_code.append(weather_data.get('weathercode')[i])
            temperature.append(weather_data.get('temperature_2m')[i])
            precipitation_probability.append(weather_data.get('precipitation_probability')[i])
            windspeed.append(weather_data.get('windspeed_10m')[i])
        return place,time,weather_code,temperature,precipitation_probability,windspeed
    
    def current_weather_precipation_probability(coordinates: list) -> int:
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=temperature_2m,precipitation_probability,weathercode,windspeed_10m&models=best_match&forecast_days=2&timezone=auto')
        response_json = response.json()
        current_time = datetime.now()
        current_hour = current_time.hour
        weather_data = response_json.get('hourly')
        for i in range(48):
            if current_hour == int(Sf.converter_date_into_hour(response_json.get('hourly').get('time')[i])):
                precipitation_probability =  weather_data.get('precipitation_probability')[i]
                return precipitation_probability

    def current_weather() -> tuple[str, int, int, int, int]:
        coordinates = geocoder.ip('me')
        latitude = round(coordinates.lat,2)
        longitude = round(coordinates.lng,2)
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&temperature,precipitation_probability,weathercode,windspeed&current_weather=true&stimezone=auto')
        response_json = response.json()
        place = Sf.place_name(latitude,longitude)
        weather = response_json.get('current_weather')
        weather_code = weather.get('weathercode')
        temperature = weather.get('temperature')
        windspeed = weather.get('windspeed')
        precipitation_probability = weather.get('precipitation_probability')
        precipitation_probability = WeatherPredictions.current_weather_precipation_probability([latitude, longitude])
        return place, weather_code, temperature, windspeed, precipitation_probability
    
    