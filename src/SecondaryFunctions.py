from geopy.geocoders import Nominatim
import requests
import json
from PIL import Image, ImageTk
import os
import datetime
from typing import Union
import tkinter as tk
import sys


class Functions:
    
    def place_name(latitude: int, longitude: int) -> str:
        response = requests.get(f'https://geocode.maps.co/reverse?lat={latitude}&lon={longitude}')
        response_json = response.json()
        address = response_json.get('address')
        if 'village' in address:
            return address.get('village')
        elif 'city' in address:
            return address.get('city')
        else:
            return address.get('county')
           
    def date_shortener(date: str) -> str:
        shorter_date = date[5:11]
        date = f'{shorter_date[3:5]}.{shorter_date[0:2]}'
        return date
    
    def converter_date_into_hour(date: str) -> str:
        hour = date[11:13]
        if hour[0] == '0':
            hour = int(hour[1])
        return hour
    
    def converter_date_into_hour2(date: str) -> str:
        hour = date[11:16]
        return hour

    def place_coordinates(city: str, state: str, country: str) -> Union[tuple[float, float], None]:
        try:
            response = requests.get(f'https://geocode.maps.co/search?city={city}&state={state}&country={country}')
            response_json = response.json()
            coordinates = response_json[0].get('boundingbox')
            coordinate_x = (float(coordinates[0])+float(coordinates[1]))/2
            coordinate_y = (float(coordinates[2])+float(coordinates[3]))/2
            return round(coordinate_x,2), round(coordinate_y,2)
        except:
            return None
            
    def weather_code_encoding(weather_code: int, wind: int, width: int, height: int) -> classmethod:
        sys.path.append('.\images')
        current_time = datetime.datetime.now()
        current_hour = int(current_time.hour)
        night_hours = [22,23,0,1,2,3,4,5]
        rainy_codes = [51,53,55,56,57,61,63,65,66,67,80,81,82]
        snowy_codes = [71,73,75,77,85,86]
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
                elif weather_code in rainy_codes:
                    img=Image.open('rainy_icon.png')
                elif weather_code in snowy_codes:
                    img=Image.open('snowy_icon.png')
            else:
                if weather_code == 0 or weather_code == 1:
                    img=Image.open('night_icon.png')
                elif weather_code == 2:
                    img=Image.open('night_cloudy_icon.png')
                elif weather_code in rainy_codes:
                    img=Image.open('night_rainy_icon.png')
                elif weather_code in snowy_codes:
                    img=Image.open('night_snowy_icon.png')
        else:
            img=Image.open('windy_icon.png')
        
        smaller_img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(smaller_img)

    def show_frame(app: classmethod, page_name: str) -> None:
        frame = app.frames[page_name]
        coordinates = Functions.place_coordinates(app.entry_buttons.city_value.get(),app.entry_buttons.state_value.get(), app.entry_buttons.country_value.get())
        if coordinates != None and not app.start_theme:
            frame.latitude = coordinates[0]
            frame.longitude = coordinates[1]
            frame.tkraise()
        elif app.start_theme:
            app.start_theme = False
            frame = app.frames['StartingFrame']
            frame.tkraise()
        else:
            frame = app.frames['IncorrectValueFrame']
            frame.tkraise()

    def weather_prediction_display(frame: classmethod, hours: list, length: int, time: list, temperature: list, precipitation_probability: list, windspeed: list) -> None:
        for i in range(length):
            frame.columnconfigure(i, weight=1)
            if hours:
                tk.Label(frame, text=Functions.converter_date_into_hour2(time[i])).grid(column=i+1, row=0)
            else:
                tk.Label(frame, text=Functions.date_shortener(time[i])).grid(column=i+1, row=0)
            tk.Label(frame, text=f'{temperature[i]}°C').grid(column=i+1, row=2)
            if precipitation_probability[i] != None:
                tk.Label(frame, text=f'{precipitation_probability[i]}%').grid(column=i+1, row=3)
            else:
                tk.Label(frame, text='soon').grid(column=i+1, row=3)
            tk.Label(frame, text=windspeed[i]).grid(column=i+1, row=4)

    def labels_display(frame: classmethod, hourly: bool) -> None:
        if hourly:
            tk.Label(frame, text='Hour: ').grid(column=0, row=0)
        else:
            tk.Label(frame, text='Date: ').grid(column=0, row=0)
        tk.Label(frame, text='Weather_code: ').grid(column=0, row=1)
        tk.Label(frame, text='Temperature: ').grid(column=0, row=2)
        tk.Label(frame, text='Precipitation probability: ').grid(column=0, row=3)
        tk.Label(frame, text='Wind speed[km/h]: ').grid(column=0, row=4)
    
            