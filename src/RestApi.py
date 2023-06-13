import requests
import json
from datetime import datetime, timedelta



def place_coordinates(city, county,country):
    response = requests.get(f'https://geocode.maps.co/search?city={city}&county={county}&country={country}')
    response_json = response.json()
    coordinates = response_json[0].get('boundingbox')
    coordinate_x = (float(coordinates[0])+float(coordinates[1]))/2
    coordinate_y = (float(coordinates[2])+float(coordinates[3]))/2
    return round(coordinate_x,2), round(coordinate_y,2)

#print(place_coordinates('Kleszczów', 'bełchatowski', 'Polska'))

def converter_data_into_hour(data):
    hour = data[11:13]
    if hour[0] == '0':
        hour = int(hour[1])
    return hour
    

def week_weather(coordinates):
    first_day = datetime.strftime(datetime.now() + timedelta(1), "%Y-%m-%d")
    last_day = datetime.strftime(datetime.now() + timedelta(7), "%Y-%m-%d")
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&daily=weathercode,temperature_2m_max,precipitation_probability_max,windspeed_10m_max&start_date={first_day}&end_date={last_day}&timezone=auto')
    response_json = response.json()
    weather_data = response_json.get('daily')
    time = weather_data.get('time')
    weather_code = weather_data.get('weathercode')
    temperature = weather_data.get('temperature_2m_max')
    precipitation_probability = weather_data.get('precipitation_probability_max')
    windspeed = weather_data.get('windspeed_10m_max')
    return time,weather_code,temperature,precipitation_probability,windspeed

#print(week_weather(place_coordinates('Kleszczów', 'bełchatowski', 'Polska')))

def hour_weather(coordinates):
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[0]}&longitude={coordinates[1]}&hourly=temperature_2m,precipitation_probability,weathercode,windspeed_10m&models=best_match&forecast_days=2&timezone=auto')
    response_json = response.json()
    current_time = datetime.now()
    current_hour = current_time.hour
    weather_data = response_json.get('hourly')
    time, weather_code, temperature, precipitation_probability, windspeed  = [],[],[],[],[]
    for i in range(48):
        if current_hour == converter_data_into_hour(response_json.get('hourly').get('time')[i]):
            index = i
            break
    for i in range(index,index+12):
        time.append(weather_data.get('time')[i])
        weather_code.append(weather_data.get('weathercode')[i])
        temperature.append(weather_data.get('temperature_2m')[i])
        precipitation_probability.append(weather_data.get('precipitation_probability')[i])
        windspeed.append(weather_data.get('windspeed_10m')[i])
    return time,weather_code,temperature,precipitation_probability,windspeed

print(hour_weather(place_coordinates('Kleszczów', 'bełchatowski', 'Polska')))
#print(datetime.now().hour)
