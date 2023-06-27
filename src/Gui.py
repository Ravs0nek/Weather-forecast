import tkinter as tk
import os
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
from Weather import WeatherPredictions as wp
from SecondaryFunctions import Functions as f
import geocoder


class app(tk.Tk):
    
    def __init__(self):
        super().__init__()
        os.chdir(r'C:\Users\milos\OneDrive\Dokumenty\GitHub\Weather-forecast\images')
        self.title('Weather forecast')
        self.iconbitmap("icon.ico")
        self.geometry('800x500+50+50')
        self.resizable(0, 0)
        self.configure(bg='LightGray')
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1,weight=2)
        self.columnconfigure(2,weight=4)
        self.frames = {}
        self.start_theme = True
        self.__create_widgets()

    def __create_widgets(self):
        PlaceNameFrame(self).grid(column = 0, row = 0, columnspan=2, sticky=tk.NSEW)
        WeatherImageFrame(self).grid(column=0, row=1, sticky=tk.W)
        CurrentWeatherFrame(self).grid(column=1, row=1, sticky=tk.NSEW)
        ImageFrame(self).grid(column = 2, row = 0, sticky=tk.E,rowspan=2)
        for F in (StartingFrame, IncorrectValueFrame, HourlyWeather, WeeklyWeather, TwoWeekWeather):
            page_name = F.__name__
            frame = F(container=self)
            self.frames[page_name] = frame
            frame.grid(column = 0, row = 3, columnspan=3, sticky=tk.NSEW)
        self.entry_buttons = EntryButtonsFrame(container=self)
        self.entry_buttons.grid(column = 0, row = 2, sticky=tk.W,columnspan=3, pady=5, padx=5)
        Functions.show_frame(app=self, page_name="StartingFrame")
        BottomFrame(self).grid(column = 0, row = 4, columnspan=3, sticky=tk.NS, pady=8)

class Functions():
    
    def show_frame(app, page_name):
        frame = app.frames[page_name]
        coordinates = f.place_coordinates(app.entry_buttons.city_value.get(),app.entry_buttons.state_value.get(), app.entry_buttons.country_value.get())
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

    def weather_prediction_display(frame, hours, length, time, temperature, precipitation_probability, windspeed):
        for i in range(length):
            frame.columnconfigure(i, weight=1)
            if hours:
                tk.Label(frame, text=f.converter_date_into_hour2(time[i])).grid(column=i+1, row=0)
            else:
                tk.Label(frame, text=f.date_shortener(time[i])).grid(column=i+1, row=0)
            tk.Label(frame, text=f'{temperature[i]}°C').grid(column=i+1, row=2)
            if precipitation_probability[i] != None:
                tk.Label(frame, text=f'{precipitation_probability[i]}%').grid(column=i+1, row=3)
            else:
                tk.Label(frame, text='soon').grid(column=i+1, row=3)
            tk.Label(frame, text=windspeed[i]).grid(column=i+1, row=4)

    def labels_display(frame, hourly):
        if hourly:
            tk.Label(frame, text='Hour: ').grid(column=0, row=0)
        else:
            tk.Label(frame, text='Date: ').grid(column=0, row=0)
        tk.Label(frame, text='Weather_code: ').grid(column=0, row=1)
        tk.Label(frame, text='Temperature: ').grid(column=0, row=2)
        tk.Label(frame, text='Precipitation probability: ').grid(column=0, row=3)
        tk.Label(frame, text='Wind speed[km/h]: ').grid(column=0, row=4)
        
class ImageFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.__create_widgets()
    
    def __create_widgets(self):
        os.chdir(r'C:\Users\milos\OneDrive\Dokumenty\GitHub\Weather-forecast\images')
        img = Image.open("weather.png")
        smaller_image = img.resize((390,300), Image.LANCZOS)#ANTIALIS
        self.img1 = ImageTk.PhotoImage(smaller_image)
        tk.Label(self, image = self.img1).grid()

class PlaceNameFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.columnconfigure(0,weight=1)
        self.__create_widgets()
    
    def __create_widgets(self):
        current_weather = wp.current_weather()
        place_name = current_weather[0]
        tk.Label(self, text=place_name, font = ('Ubuntu', 30, 'bold'), background='LightGray').grid(column=0, row=0, sticky=tk.NSEW, pady=25)

class WeatherImageFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        current_weather = wp.current_weather()
        weather_code, wind_speed = current_weather[1], current_weather[4]
        self.img = f.weather_code_encoding(weather_code, wind_speed, 250,200)
        tk.Label(self, image = self.img).grid()

class CurrentWeatherFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.__create_widgets()

    def __create_widgets(self):
        current_weather = wp.current_weather()
        temperature,wind_speed,precipitation_probability = current_weather[2],current_weather[3],current_weather[4]
        tk.Label(self, text='Temperature: ', background='LightGray',font = ('Ubuntu', 10, 'bold')).grid(row=0)
        tk.Label(self, text=str(temperature)+'℃', background='LightGray').grid(row=1)
        tk.Label(self, text='Precipitation probability: ', background='LightGray',font = ('Ubuntu', 10, 'bold')).grid(row=2)
        tk.Label(self, text=str(precipitation_probability)+'%', background='LightGray').grid(row=3)
        tk.Label(self, text='Wind Speed:', background='LightGray',font = ('Ubuntu', 10, 'bold')).grid(row=4)
        tk.Label(self, text=str(wind_speed)+'km/h', background='LightGray').grid(row=5)

class HourlyWeather(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
    
    def __create_widgets(self):
        place_coordinates = geocoder.ip('me')
        self.latitude = round(place_coordinates.lat,2)
        self.longitude = round(place_coordinates.lng,2)           
        hourly_weather_data = wp.hourly_weather([self.latitude,self.longitude])
        time,weather_code,temperature,precipitation_probability,windspeed = hourly_weather_data[1], hourly_weather_data[2], hourly_weather_data[3], hourly_weather_data[4], hourly_weather_data[5]
        Functions.labels_display(self,True)
        self.img0, self.img1,self.img2,self.img3,self.img4,self.img5,self.img6,self.img7,self.img8,self.img9,self.img10,self.img11 = f.weather_code_encoding(weather_code[0], windspeed[0],25,25),f.weather_code_encoding(weather_code[1], windspeed[1],25,25),f.weather_code_encoding(weather_code[2], windspeed[2],25,25), f.weather_code_encoding(weather_code[3], windspeed[3],25,25), f.weather_code_encoding(weather_code[4], windspeed[4],25,25), f.weather_code_encoding(weather_code[5], windspeed[5],25,25), f.weather_code_encoding(weather_code[6], windspeed[6],25,25), f.weather_code_encoding(weather_code[7], windspeed[7],25,25), f.weather_code_encoding(weather_code[8], windspeed[8],25,25), f.weather_code_encoding(weather_code[9], windspeed[9],25,25), f.weather_code_encoding(weather_code[10], windspeed[10],25,25), f.weather_code_encoding(weather_code[11], windspeed[11],25,25)
        Functions.weather_prediction_display(self, True, len(time),time,temperature,precipitation_probability,windspeed)
        for i in range(len(time)):
            tk.Label(self, image=eval('self.img' + str(i))).grid(column=i+1, row=1)

class WeeklyWeather(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()
    
    def __create_widgets(self):
        place_coordinates = geocoder.ip('me')
        self.latitude = round(place_coordinates.lat,2)
        self.longitude = round(place_coordinates.lng,2)   
        weekly_weather_data = wp.week_weather([self.latitude,self.longitude])
        time,weather_code,temperature,precipitation_probability,windspeed = weekly_weather_data[1], weekly_weather_data[2], weekly_weather_data[3], weekly_weather_data[4], weekly_weather_data[5]
        Functions.labels_display(self,False)
        self.img0, self.img1,self.img2,self.img3,self.img4,self.img5,self.img6 = f.weather_code_encoding(weather_code[0], windspeed[0],25,25),f.weather_code_encoding(weather_code[1], windspeed[1],25,25),f.weather_code_encoding(weather_code[2], windspeed[2],25,25), f.weather_code_encoding(weather_code[3], windspeed[3],25,25), f.weather_code_encoding(weather_code[4], windspeed[4],25,25), f.weather_code_encoding(weather_code[5], windspeed[5],25,25), f.weather_code_encoding(weather_code[6], windspeed[6],25,25)
        Functions.weather_prediction_display(self, False, len(time),time,temperature,precipitation_probability,windspeed)
        for i in range(len(time)):
            tk.Label(self, image=eval('self.img' + str(i))).grid(column=i+1, row=1)

class TwoWeekWeather(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.__create_widgets()

    def __create_widgets(self):
        place_coordinates = geocoder.ip('me')
        self.latitude = round(place_coordinates.lat,2)
        self.longitude = round(place_coordinates.lng,2)   
        two_week_weather_data = wp.two_week_weather([self.latitude,self.longitude])
        time,weather_code,temperature,precipitation_probability,windspeed = two_week_weather_data[1], two_week_weather_data[2], two_week_weather_data[3], two_week_weather_data[4], two_week_weather_data[5]
        Functions.labels_display(self,False)
        self.img0, self.img1,self.img2,self.img3,self.img4,self.img5,self.img6,self.img7,self.img8,self.img9,self.img10,self.img11,self.img12,self.img13 = f.weather_code_encoding(weather_code[0], windspeed[0],25,25),f.weather_code_encoding(weather_code[1], windspeed[1],25,25),f.weather_code_encoding(weather_code[2], windspeed[2],25,25), f.weather_code_encoding(weather_code[3], windspeed[3],25,25), f.weather_code_encoding(weather_code[4], windspeed[4],25,25), f.weather_code_encoding(weather_code[5], windspeed[5],25,25), f.weather_code_encoding(weather_code[6], windspeed[6],25,25), f.weather_code_encoding(weather_code[7], windspeed[7],25,25), f.weather_code_encoding(weather_code[8], windspeed[8],25,25), f.weather_code_encoding(weather_code[9], windspeed[9],25,25), f.weather_code_encoding(weather_code[10], windspeed[10],25,25), f.weather_code_encoding(weather_code[11], windspeed[11],25,25), f.weather_code_encoding(weather_code[12], windspeed[12],25,25),f.weather_code_encoding(weather_code[13], windspeed[13],25,25)
        Functions.weather_prediction_display(self, False, len(time),time,temperature,precipitation_probability,windspeed)
        for i in range(len(time)):
            tk.Label(self, image=eval('self.img' + str(i))).grid(column=i+1, row=1)


class EntryButtonsFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.configure(bg='LightGray')
        self.city_value, self.state_value, self.country_value, self.type_of_weather = tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.__create_widgets()
    
    def __create_widgets(self):
        tk.Label(self, text='City: ', background='LightGray',font = ('Ubuntu' , 10, 'bold')).grid(column=0, row=0, padx = 5)
        self.city_entry = tk.Entry(self, textvariable=self.city_value)
        self.city_entry.grid(column=1, row=0, padx = 5)
        tk.Label(self, text='State: ', background='LightGray',font = ('Ubuntu' , 10, 'bold')).grid(column=2, row=0, padx = 5)
        self.state_entry = tk.Entry(self, textvariable=self.state_value)
        self.state_entry.grid(column=3, row=0, padx = 5)
        tk.Label(self, text='Country: ', background='LightGray',font = ('Ubuntu' , 10, 'bold')).grid(column=4, row=0, padx = 5)
        self.country_entry = tk.Entry(self, textvariable=self.country_value)
        self.country_entry.grid(column=5, row=0, padx = 5)
        tk.Button(self, text = 'Enter', command = lambda: Functions.show_frame(self.container, self.type_of_weather.get())).grid(column=6, row=0, padx=5)
        tk.Button(self, text = 'Clear', command = lambda: self.clear_entries()).grid(column=7, row=0, padx=5)
        weather_type_box = ttk.Combobox(self, textvariable=self.type_of_weather, state='readonly')
        weather_type_box['values'] = ('HourlyWeather', 'WeeklyWeather', 'TwoWeekWeather')
        weather_type_box.current(0)
        weather_type_box.grid(column=8, row=0, padx=5)

    def clear_entries(self):
        for entry in (self.city_entry,self.state_entry,self.country_entry):
            entry.delete(0, 'end')

class StartingFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='Enter location properties',font = ('Ubuntu' , 35, 'underline'), background='LightGray').pack(anchor='center', pady=15)

class IncorrectValueFrame(tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='Enter correct properties',font = ('Ubuntu' , 35, 'underline'), background='LightGray').pack(anchor='center', pady=15)

class BottomFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.configure(bg='LightGray')
        self.__create_widgets()
    
    def __create_widgets(self):
        self.rowconfigure(0, weight=1)
        tk.Label(self, text='Thanks for using our weather forecast!', font = ('Ubuntu' , 25), background='LightGray').grid(row=0, sticky=tk.NSEW)


