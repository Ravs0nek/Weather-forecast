import sys
sys.path.append('./src')
from Weather import WeatherPredictions as wp

def test_week_weather():
    warsaw_latitude = 52.23
    warsaw_longitude = 21
    week_weather_predictions = wp.week_weather([warsaw_latitude,warsaw_longitude])
    place_name,dates,weather_codes,temperatures,precipitation_probabilities,windspeeds = week_weather_predictions[0],week_weather_predictions[1], week_weather_predictions[2],week_weather_predictions[3],week_weather_predictions[4],week_weather_predictions[5]
    assert place_name == 'Warsaw' and len(dates) == 7 and len(weather_codes) == 7 and len(temperatures) == 7 and len(precipitation_probabilities) == 7 and len(windspeeds) == 7

def test_two_week_weather():
    poznan_latitude = 52.4
    poznan_longitude = 16.93
    two_week_weather_predictions = wp.two_week_weather([poznan_latitude,poznan_longitude])
    place_name,dates,weather_codes,temperatures,precipitation_probabilities,windspeeds = two_week_weather_predictions[0],two_week_weather_predictions[1], two_week_weather_predictions[2],two_week_weather_predictions[3],two_week_weather_predictions[4],two_week_weather_predictions[5]
    assert place_name == 'Poznań' and len(dates) == 14 and len(weather_codes) == 14 and len(temperatures) == 14 and len(precipitation_probabilities) == 14 and len(windspeeds) == 14

def test_hourly_weather():
    wroclaw_latitude = 51.1
    wroclaw_longitude = 17.03
    hourly_weather_predictions = wp.hourly_weather([wroclaw_latitude,wroclaw_longitude])
    place_name,dates,weather_codes,temperatures,precipitation_probabilities,windspeeds = hourly_weather_predictions[0],hourly_weather_predictions[1], hourly_weather_predictions[2],hourly_weather_predictions[3],hourly_weather_predictions[4],hourly_weather_predictions[5]
    assert place_name == 'Wrocław' and len(dates) == 12 and len(weather_codes) == 12 and len(temperatures) == 12 and len(precipitation_probabilities) == 12 and len(windspeeds) == 12

def test_current_weather_precipation_probability():
    lodz_latitude = 51.76
    lodz_longitude = 19.45
    current_weather_precipation_probability_predictions = wp.current_weather_precipation_probability([lodz_latitude,lodz_longitude])
    assert type(current_weather_precipation_probability_predictions) == int

def test_current_weather():
    current_weather_prediction = wp.current_weather()
    place_name,weather_code,temperature,precipitation_probability,windspeed = current_weather_prediction[0],current_weather_prediction[1], current_weather_prediction[2],current_weather_prediction[3],current_weather_prediction[4]
    assert type(place_name) == str and type(weather_code) == int and type(temperature) == float and type(precipitation_probability) == float and type(windspeed) == int


