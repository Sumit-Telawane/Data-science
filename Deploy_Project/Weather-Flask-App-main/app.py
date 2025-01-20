import json
import requests
from flask import Flask, request, render_template

API_KEY = "ea642ff5d0165717d77c25f8bdb605da"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_weather', methods=['POST'])
def predict_weather():
    if request.method == 'POST':
        q = request.form['location']
        querystring = {"q": q, "appid": API_KEY, "units": "metric"}  # 'units': 'metric' gives temperatures in Celsius
        
        try:
            response = requests.get(API_URL, params=querystring)
            print(response.text)
            json_data = json.loads(response.text)

            # Parsing the JSON response
            name = json_data['name']
            country = json_data['sys']['country']
            lat = json_data['coord']['lat']
            lon = json_data['coord']['lon']
            temp_c = json_data['main']['temp']
            feels_like_c = json_data['main']['feels_like']
            temp_min_c = json_data['main']['temp_min']
            temp_max_c = json_data['main']['temp_max']
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind_speed = json_data['wind']['speed']
            wind_degree = json_data['wind']['deg']
            weather_description = json_data['weather'][0]['description']
            icon = json_data['weather'][0]['icon']

            # Pass the data to the template
            return render_template('home.html', name=name, country=country, lat=lat, lon=lon, temp_c=temp_c, 
                                   feels_like_c=feels_like_c, temp_min_c=temp_min_c, temp_max_c=temp_max_c,
                                   pressure=pressure, humidity=humidity, wind_speed=wind_speed, wind_degree=wind_degree,
                                   weather_description=weather_description, icon=icon)

        except Exception as e:
            print(e)
            return render_template('home.html', error='Please enter a correct location name.')

if __name__ == '__main__':
    app.run(debug=True)
