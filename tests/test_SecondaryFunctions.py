from src.SecondaryFunctions import Functions as f
import tkinter as tk
from PIL import Image, ImageTk

def test_place_name():
    warsaw_latitude = 52.25
    warsaw_longitude = 21
    results = f.place_name(warsaw_latitude,warsaw_longitude)
    assert results == 'Warszawa'

def test_date_shortener():
    date = '2023-06-16T17:31'
    short_date = f.date_shortener(date)
    assert short_date == '16.06'

def test_converter_date_into_hour():
    date = '2023-06-16T17:31'
    hour = f.converter_date_into_hour(date)
    assert hour == '17'

def test_converter_date_into_hour2():
    date = '2023-06-16T17:31'
    hour = f.converter_date_into_hour2(date)
    assert hour == '17:31'

def test_place_coordinates():
    city = 'kleszczów'
    county = 'bełchatowski'
    country = 'polska'
    assert f.place_coordinates(city,county,country) == (51.22,19.3)

def test_weather_code_encoding():
    weather_code= 2
    wind = 20
    root = tk.Tk()
    photo = f.weather_code_encoding(weather_code, wind,25,25)
    assert photo.height() == 25, photo.weidth() == 25

    
    