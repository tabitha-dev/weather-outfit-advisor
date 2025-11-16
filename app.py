from flask import Flask, render_template, jsonify, request
import urllib.request
import json

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static',
            static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    city = request.args.get('city', 'Redmond')
    
    try:
        # Using Open-Meteo (free, no API key needed!)
        coords = {
            'Redmond': (47.6740, -122.1215),
            'Seattle': (47.6062, -122.3321),
            'Denver': (39.7392, -104.9903),
            'Austin': (30.2672, -97.7431),
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437)
        }
        
        if city not in coords:
            coords[city] = (47.6740, -122.1215)  # default to Redmond
        
        lat, lon = coords[city]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&temperature_unit=fahrenheit"
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            current = data['current']
            temp = current['temperature_2m']
            
            # Simple weather descriptions
            weather_codes = {
                0: 'Clear sky',
                1: 'Partly cloudy',
                2: 'Overcast',
                3: 'Overcast',
                45: 'Foggy',
                48: 'Foggy',
                51: 'Light drizzle',
                53: 'Moderate drizzle',
                55: 'Dense drizzle',
                61: 'Slight rain',
                63: 'Moderate rain',
                65: 'Heavy rain',
                71: 'Slight snow',
                73: 'Moderate snow',
                75: 'Heavy snow',
                80: 'Slight rain showers',
                81: 'Moderate rain showers',
                82: 'Violent rain showers',
                85: 'Slight snow showers',
                86: 'Heavy snow showers',
                95: 'Thunderstorm',
                96: 'Thunderstorm with hail',
                99: 'Thunderstorm with hail'
            }
            
            condition = weather_codes.get(current['weather_code'], 'Partly cloudy')
            
            return jsonify({
                'temperature': round(temp, 1),
                'feels_like': round(temp - 2, 1),
                'condition': condition,
                'city': city
            })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'temperature': 65.0,
            'feels_like': 63.0,
            'condition': 'partly cloudy',
            'city': city
        })

@app.route('/api/outfit')
def get_outfit():
    temp = float(request.args.get('temperature', 65))
    
    if temp < 40:
        items = [
            {'name': 'Winter Coat', 'category': 'Outerwear', 'description': 'Heavy insulation'},
            {'name': 'Thermal Base', 'category': 'Tops', 'description': 'Keep warm'},
            {'name': 'Wool Pants', 'category': 'Bottoms', 'description': 'Warm'},
            {'name': 'Winter Boots', 'category': 'Footwear', 'description': 'Insulated'},
            {'name': 'Beanie', 'category': 'Accessories', 'description': 'Head warmth'},
        ]
    elif temp < 60:
        items = [
            {'name': 'Light Jacket', 'category': 'Outerwear', 'description': 'Perfect fit'},
            {'name': 'Long Sleeve', 'category': 'Tops', 'description': 'Comfortable'},
            {'name': 'Jeans', 'category': 'Bottoms', 'description': 'Classic'},
            {'name': 'Sneakers', 'category': 'Footwear', 'description': 'Comfy'},
        ]
    elif temp < 75:
        items = [
            {'name': 'T-Shirt', 'category': 'Tops', 'description': 'Light'},
            {'name': 'Pants', 'category': 'Bottoms', 'description': 'Casual'},
            {'name': 'Sneakers', 'category': 'Footwear', 'description': 'Perfect'},
        ]
    else:
        items = [
            {'name': 'Tank Top', 'category': 'Tops', 'description': 'Cool'},
            {'name': 'Shorts', 'category': 'Bottoms', 'description': 'Breezy'},
            {'name': 'Sandals', 'category': 'Footwear', 'description': 'Easy'},
        ]
    
    return jsonify({'items': items})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', 'hi')
    
    if 'formal' in message.lower():
        response = "Dress shirt with blazer and dress pants!"
    elif 'hike' in message.lower():
        response = "Great for hiking! Layers, boots, and water!"
    elif 'beach' in message.lower():
        response = "Perfect beach! Swimsuit, sunscreen, and cover-up!"
    else:
        response = "That sounds great!"
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
