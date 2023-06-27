from geopy.geocoders import Nominatim
import requests
import json
from PIL import Image, ImageTk
import os
import datetime

class Functions:
    
    def place_name(latitude, longitude):
        response = requests.get(f'https://geocode.maps.co/reverse?lat={latitude}&lon={longitude}')
        response_json = response.json()
        address = response_json.get('address')
        if 'village' in address:
            return address.get('village')
        elif 'city' in address:
            return address.get('city')
        else:
            return address.get('county')
           
    def date_shortener(date):
        shorter_date = date[5:11]
        date = f'{shorter_date[3:5]}.{shorter_date[0:2]}'
        return date
    
    def converter_date_into_hour(date):
        hour = date[11:13]
        if hour[0] == '0':
            hour = int(hour[1])
        return hour
    
    def converter_date_into_hour2(date):
        hour = date[11:16]
        return hour

    def place_coordinates(city, state,country):
        try:
            response = requests.get(f'https://geocode.maps.co/search?city={city}&state={state}&country={country}')
            response_json = response.json()
            coordinates = response_json[0].get('boundingbox')
            coordinate_x = (float(coordinates[0])+float(coordinates[1]))/2
            coordinate_y = (float(coordinates[2])+float(coordinates[3]))/2
            return round(coordinate_x,2), round(coordinate_y,2)
        except:
            return None
            
    def weather_code_encoding(weather_code, wind, width, height):
        os.chdir(r'C:\Users\milos\OneDrive\Dokumenty\GitHub\Weather-forecast\images')
        current_time = datetime.datetime.now()
        current_hour = int(current_time.hour)
        night_hours = [22,23,0,1,2,3,4,5]
        if wind == None:
            wind = 0
        if wind < 60:
            if weather_code == 3:
                img=Image.open('cloudy_icon.png')
            elif weather_code == 45 or weather_code == 48:
                img=Image.open('foggy_icon.png')
            elif weather_code == 95 or weather_code == 96 or weather_code == 99:
                img=Image.open('stormy_icon.png')
            if current_hour not in night_hours:
                if weather_code == 0 or weather_code == 1:
                    img=Image.open('sunny_icon.png')
                elif weather_code == 2:
                    img=Image.open('sunny_cloudy_icon.png')
                elif weather_code == 51 or weather_code == 53 or weather_code == 55 or weather_code == 56 or weather_code == 57 or weather_code == 61 or weather_code == 63 or weather_code == 65 or weather_code == 66 or weather_code == 67 or weather_code == 80 or weather_code == 81 or weather_code == 82:
                    img=Image.open('rainy_icon.png')
                elif weather_code == 71 or weather_code == 73 or weather_code == 75 or weather_code == 77 or weather_code == 85 or weather_code == 86:
                    img=Image.open('snowy_icon.png')
            else:
                if weather_code == 0 or weather_code == 1:
                    img=Image.open('night_icon.png')
                elif weather_code == 2:
                    img=Image.open('night_cloudy_icon.png')
                elif weather_code == 51 or weather_code == 53 or weather_code == 55 or weather_code == 56 or weather_code == 57 or weather_code == 61 or weather_code == 63 or weather_code == 65 or weather_code == 66 or weather_code == 67 or weather_code == 80 or weather_code == 81 or weather_code == 82:
                    img=Image.open('night_rainy_icon.png')
                elif weather_code == 71 or weather_code == 73 or weather_code == 75 or weather_code == 77 or weather_code == 85 or weather_code == 86:
                    img=Image.open('night_snowy_icon.png')
        else:
            img=Image.open('windy_icon.png')
        
        smaller_img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(smaller_img)
    
    
            