from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_google_geocode(address):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    getparams = {
        'address': address,
        'key': api_key
    }
    response = requests.get(url, params=getparams)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            return {
                'formatted_address': result['formatted_address'],
                'latitude': result['geometry']['location']['lat'],
                'longitude': result['geometry']['location']['lng']
            }
    return None

def get_weather(lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')  
    
    if not api_key:
        print("API key not found.")
        return None

    url = 'https://api.openweathermap.org/data/2.5/weather'
    getparams = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'  
    }

    response = requests.get(url, params=getparams)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json()}")

    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data:
            weather_info = {
                'temperature': data['main'].get('temp', 'N/A'),
                'description': data['weather'][0].get('description', 'N/A'),
                'humidity': data['main'].get('humidity', 'N/A'),
                'wind_speed': data['wind'].get('speed', 'N/A')
            }
            return weather_info
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return None

@app.route('/')
def FrontPage():
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('Front_Page.html', api_key=google_maps_api_key)

@app.route('/geocode', methods=['POST'])
def geocode():
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    from_address = request.form['from_address']
    to_address = request.form['to_address']
    
    from_location = get_google_geocode(from_address)
    to_location = get_google_geocode(to_address)

    from_weather = None
    to_weather = None
    if from_location:
        from_weather = get_weather(from_location['latitude'], from_location['longitude'])
    if to_location:
        to_weather = get_weather(to_location['latitude'], to_location['longitude'])

    return render_template('Main_Page.html', 
                            from_location=from_location, 
                            to_location=to_location, 
                            from_weather=from_weather, 
                            to_weather=to_weather, 
                            api_key=google_maps_api_key)

if __name__ == '__main__':
    app.run(debug=True)
