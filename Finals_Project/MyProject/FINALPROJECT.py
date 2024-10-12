from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_google_geocode(address):
    api_key = ''
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

@app.route('/')
def FrontPage():
    return render_template('Front_Page.html')

@app.route('/geocode', methods=['POST'])
def geocode():
    from_address = request.form['from_address']
    to_address = request.form['to_address']
    
    from_location = get_google_geocode(from_address)
    to_location = get_google_geocode(to_address)

    return render_template('Main_Page.html', from_location=from_location, to_location=to_location)

if __name__ == '__main__':
    app.run(debug=True)