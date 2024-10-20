from flask import Flask, render_template, request   # Import necessary Flask modules
import requests                                     # Used to send HTTP requests to external APIs
import os                                           # For interacting with the operating system
from dotenv import load_dotenv                      # For loading environment variables from a .env file

load_dotenv() # to load the env file created


app = Flask(__name__)   #get initialize the flask app library


#Function to get google maps geocoding api (location data)
def get_google_geocode(address):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  #get the api key from .env(environment variables) file to load

    # Return None if API key is missing
    if not api_key:
        print("Google maps API key not found.")
        return None
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json' # geocoding api url

    # Parameters to send to Google Geocoding API
    getparams = {
        'address': address,
        'key': api_key
    }

    response = requests.get(url, params=getparams) #Send request to Google Geocoding API
    
     # If response is successful it iniatilize getting the informations
    if response.status_code == 200:
        data = response.json()          # Parse the JSON response
        if data['results']:             # Check if results exist
            result = data['results'][0] # Get the first result
            return {
                'formatted_address': result['formatted_address'],   # get the formatted address
                'latitude': result['geometry']['location']['lat'],  # get the latitude
                'longitude': result['geometry']['location']['lng']  # get the longitude
            }
    return None     # return non if no valid data 


# Function to get weather data based on latitude and longitude using OpenWeatherMap API
def get_weather(lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY') #get the api key from .env(environment variables) file to load
    
    # Return None if API key is missing
    if not api_key:
        print("Open Weather API key not found.")
        return None

    url = 'https://api.openweathermap.org/data/2.5/weather'

    # Parameters to send to OpenWeather Api
    getparams = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'  
    }

    response = requests.get(url, params=getparams) #Send request to Google Geocoding API
    
    # If response is successful it iniatilize getting the informations
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data:
            weather_info = {
                'temperature': data['main'].get('temp', 'N/A'),                 #get the temperature
                'description': data['weather'][0].get('description', 'N/A'),    #get the description of weather
                'humidity': data['main'].get('humidity', 'N/A'),                #get the humidity
                'wind_speed': data['wind'].get('speed', 'N/A')                  #get the wind speed
            }
            return weather_info # Return the weather information
    else:
        print(f"Error: {response.status_code} - {response.text}")  # error handling if request data fail
    return None # return none if no valid data

#location of the front page to get the access
@app.route('/')
def FrontPage():
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY') #get the api key from .env(environment variables) file to load
    return render_template('Front_Page.html', api_key=google_maps_api_key)  # Render the front page template

# Route to handle geocoding and weather api fetching based on user input
@app.route('/geocode', methods=['POST'])
def geocode():
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY') #get the api key from .env(environment variables) file to load
    from_address = request.form['from_address'] # get the "From" address of user input
    to_address = request.form['to_address']     # get the "to" address of user input
    
    from_location = get_google_geocode(from_address) # Get geocode for 'from' address
    to_location = get_google_geocode(to_address)     # Get geocode for 'to' address

    from_weather = None
    to_weather = None

    # get weather data for 'from' location if geocode data is available
    if from_location:
        from_weather = get_weather(from_location['latitude'], from_location['longitude'])
    # get weather data for 'to' location if geocode data is available
    if to_location:
        to_weather = get_weather(to_location['latitude'], to_location['longitude'])

     # Render the main page template with the locations and weather data
    return render_template('Main_Page.html', 
                            from_location=from_location, 
                            to_location=to_location, 
                            from_weather=from_weather, 
                            to_weather=to_weather, 
                            api_key=google_maps_api_key)

# Main block to run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
