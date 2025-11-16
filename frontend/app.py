"""
Frontend Web Server for Weather Outfit ADK

Simple Flask app that serves the UI and proxies requests to the ADK Coach agent.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS

# Add parent directory to path to import weather_outfit_adk
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_outfit_adk.monitoring import setup_logging, agent_metrics
from weather_outfit_adk.tools.weather_tools import get_current_weather
from outfit_generator import generate_comprehensive_outfit

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Setup logging
logger = setup_logging("frontend", enable_cloud_logging=False)

# In-memory session storage for tracking (demo purposes)
sessions = {}

# Weather data cache with TTL (5 minutes)
from datetime import datetime, timedelta
weather_cache = {}
WEATHER_CACHE_TTL = timedelta(minutes=5)

# ADK Coach Agent configuration
import requests
import uuid
COACH_AGENT_URL = os.getenv("COACH_AGENT_URL", "http://localhost:8000")
USE_ADK_AGENTS = os.getenv("USE_ADK_AGENTS", "true").lower() == "true"

def call_coach_agent(message, user_id=None, session_id=None):
    """
    Call the Coach Agent via A2A protocol
    
    Args:
        message: Natural language query for the agent
        user_id: Unique user identifier
        session_id: Session ID for conversation context
        
    Returns:
        dict: Agent response with outfit recommendations
    """
    if not USE_ADK_AGENTS:
        logger.info("ADK agents disabled, using direct functions")
        return None
    
    if not user_id:
        user_id = str(uuid.uuid4())
    if not session_id:
        session_id = str(uuid.uuid4())
    
    try:
        logger.info(f"Calling Coach Agent: {message}")
        
        # Call Coach Agent A2A endpoint
        response = requests.post(
            f"{COACH_AGENT_URL}/run",
            json={
                "user_id": user_id,
                "session_id": session_id,
                "message": message
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Coach Agent response received")
            return result
        else:
            logger.error(f"Coach Agent error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        logger.warning(f"Cannot connect to Coach Agent at {COACH_AGENT_URL}. Using fallback.")
        return None
    except Exception as e:
        logger.error(f"Error calling Coach Agent: {str(e)}")
        return None

def get_cached_weather(city):
    """Get cached weather data if available and not expired"""
    city_key = city.lower().strip()
    if city_key in weather_cache:
        cached_data, timestamp = weather_cache[city_key]
        if datetime.now() - timestamp < WEATHER_CACHE_TTL:
            logger.info(f"Using cached weather data for {city}")
            return cached_data
    return None

def cache_weather_data(city, data):
    """Cache weather data with timestamp"""
    city_key = city.lower().strip()
    weather_cache[city_key] = (data, datetime.now())
    logger.info(f"Cached weather data for {city}")

import random


def generate_outfit_items_with_preferences(temperature, condition, style, clothing_types, colors):
    """Generate outfit items based on temperature, conditions, and user preferences"""
    items = []
    
    # Determine style modifiers
    is_minimalist = any('minimalist' in s.lower() for s in style)
    is_formal = any('formal' in s.lower() for s in style)
    is_casual = any('casual' in s.lower() for s in style)
    is_sporty = any('sporty' in s.lower() or 'athletic' in s.lower() for s in style)
    
    # Determine color preferences
    color_palette = ''.join(colors).lower()
    prefers_neutral = 'neutral' in color_palette
    prefers_blues = 'blues' in color_palette or 'blue' in color_palette
    prefers_earth = 'earth' in color_palette
    prefers_bold = 'bold' in color_palette or 'bright' in color_palette
    
    # Helper to add color description
    def get_color_desc():
        if prefers_blues:
            return "in navy or blue tones"
        elif prefers_earth:
            return "in earth tones"
        elif prefers_bold:
            return "in vibrant colors"
        elif prefers_neutral:
            return "in neutral tones"
        else:
            return "in your preferred colors"
    
    # Outerwear
    if temperature < 40:
        if is_formal:
            items.append({
                "category": "Outerwear",
                "name": "Wool Coat",
                "description": f"Tailored {get_color_desc()}"
            })
        else:
            coat_color = "navy" if prefers_blues else "charcoal" if prefers_neutral else "brown" if prefers_earth else "black"
            items.append({
                "category": "Outerwear",
                "name": "Heavy Coat",
                "description": f"{coat_color.capitalize()} winter coat"
            })
    elif temperature < 60:
        if 'denim' in ''.join(clothing_types).lower() or 'jackets' in ''.join(clothing_types).lower():
            jacket_style = "denim" if not is_formal else "khaki"
            items.append({
                "category": "Outerwear",
                "name": "Light Jacket",
                "description": f"{jacket_style.capitalize()} jacket"
            })
        else:
            items.append({
                "category": "Outerwear",
                "name": "Light Jacket",
                "description": f"Casual layer {get_color_desc()}"
            })
    else:
        if not is_minimalist:
            cardigan_color = "blue" if prefers_blues else "beige" if prefers_neutral else "olive" if prefers_earth else "gray"
            items.append({
                "category": "Outerwear",
                "name": "Light Cardigan",
                "description": f"{cardigan_color.capitalize()} cardigan"
            })
    
    # Top
    if temperature < 50:
        shirt_color = "navy" if prefers_blues else "white or gray" if prefers_neutral else "olive" if prefers_earth else "colorful"
        items.append({
            "category": "Top",
            "name": "Long-Sleeve Shirt",
            "description": f"{shirt_color.capitalize()} cotton"
        })
    else:
        tee_color = "blue" if prefers_blues else "white or black" if prefers_neutral else "rust or tan" if prefers_earth else "any color"
        items.append({
            "category": "Top",
            "name": "T-Shirt",
            "description": f"{tee_color.capitalize()} tee"
        })
    
    # Bottoms
    if 'jeans' in ''.join(clothing_types).lower():
        jean_wash = "dark wash" if prefers_blues or is_formal else "medium wash" if prefers_neutral else "light wash"
        items.append({
            "category": "Bottoms",
            "name": "Jeans",
            "description": f"{jean_wash.capitalize()} denim"
        })
    elif temperature < 45:
        pant_color = "navy" if prefers_blues else "gray or black" if prefers_neutral else "brown" if prefers_earth else "dark"
        items.append({
            "category": "Bottoms",
            "name": "Warm Pants",
            "description": f"{pant_color.capitalize()} insulated"
        })
    else:
        pant_color = "khaki" if prefers_earth or prefers_neutral else "navy" if prefers_blues else "chino"
        items.append({
            "category": "Bottoms",
            "name": "Casual Pants",
            "description": f"{pant_color.capitalize()} comfort"
        })
    
    # Footwear
    if 'rain' in condition.lower() or temperature < 40:
        boot_color = "brown" if prefers_earth else "black"
        items.append({
            "category": "Footwear",
            "name": "Waterproof Boots",
            "description": f"{boot_color.capitalize()} boots"
        })
    elif 'sneakers' in ''.join(clothing_types).lower():
        sneaker_color = "white" if prefers_neutral or is_minimalist else "navy" if prefers_blues else "any color"
        items.append({
            "category": "Footwear",
            "name": "Sneakers",
            "description": f"{sneaker_color.capitalize()} sneakers"
        })
    else:
        shoe_color = "brown" if prefers_earth else "black" if prefers_neutral else "navy" if prefers_blues else "casual"
        items.append({
            "category": "Footwear",
            "name": "Casual Shoes",
            "description": f"{shoe_color.capitalize()} shoes"
        })
    
    # Add accessories based on conditions
    # Sunglasses for sunny/warm weather
    if temperature > 70 or 'sunny' in condition.lower() or 'clear' in condition.lower():
        sunglass_style = "aviators" if prefers_neutral else "wayfarers" if prefers_bold else "classic"
        items.append({
            "category": "Sunglasses",
            "name": "Sunglasses",
            "description": f"{sunglass_style.capitalize()} for sun protection"
        })
    
    # Winter hat for cold weather
    if temperature < 45:
        hat_color = "gray" if prefers_neutral else "navy" if prefers_blues else "brown" if prefers_earth else "warm"
        items.append({
            "category": "Accessory",
            "name": "Winter Hat",
            "description": f"{hat_color.capitalize()} beanie or cap"
        })
    
    # Scarf for cold or windy weather
    if temperature < 50:
        scarf_color = "neutral" if prefers_neutral else "blue" if prefers_blues else "earth tone" if prefers_earth else "colorful"
        items.append({
            "category": "Accessory",
            "name": "Scarf",
            "description": f"{scarf_color.capitalize()} knit scarf"
        })
    
    # Umbrella for rainy weather
    if 'rain' in condition.lower():
        items.append({
            "category": "Accessory",
            "name": "Umbrella",
            "description": "Compact waterproof umbrella"
        })
    
    # General accessory for moderate weather
    if 'rain' not in condition.lower() and 50 <= temperature <= 75:
        accessory_color = "silver" if prefers_neutral else "gold" if prefers_earth or prefers_bold else "minimal"
        items.append({
            "category": "Accessory",
            "name": "Watch or Bracelet",
            "description": f"{accessory_color.capitalize()} accent"
        })
    
    # Gloves for very cold weather
    if temperature < 35:
        glove_color = "black" if prefers_neutral else "brown" if prefers_earth else "warm"
        items.append({
            "category": "Accessory",
            "name": "Gloves",
            "description": f"{glove_color.capitalize()} insulated gloves"
        })
    
    # Add more items based on style preferences to reach 6-8 items
    current_count = len(items)
    
    # Add bag/backpack for casual/sporty styles
    if (is_casual or is_sporty) and current_count < 7:
        bag_color = "navy" if prefers_blues else "brown" if prefers_earth else "black" if prefers_neutral else "canvas"
        items.append({
            "category": "Accessory",
            "name": "Backpack or Bag",
            "description": f"{bag_color.capitalize()} crossbody or backpack"
        })
        current_count += 1
    
    # Add belt for formal/minimalist styles
    if (is_formal or is_minimalist) and current_count < 7:
        belt_color = "brown" if prefers_earth else "black"
        items.append({
            "category": "Accessory",
            "name": "Belt",
            "description": f"{belt_color.capitalize()} leather belt"
        })
        current_count += 1
    
    # Add layering piece if cold and not already at max
    if temperature < 55 and current_count < 7:
        layer_color = "gray" if prefers_neutral else "navy" if prefers_blues else "olive" if prefers_earth else "neutral"
        items.append({
            "category": "Top",
            "name": "Base Layer",
            "description": f"{layer_color.capitalize()} thermal or cotton layer"
        })
        current_count += 1
    
    # Add socks recommendation for complete outfit
    if current_count < 8:
        sock_style = "wool" if temperature < 50 else "cotton" if temperature < 70 else "athletic"
        sock_color = "dark" if prefers_neutral or prefers_blues else "earth tone" if prefers_earth else "casual"
        items.append({
            "category": "Accessory",
            "name": "Socks",
            "description": f"{sock_color.capitalize()} {sock_style} socks"
        })
    
    return items


def generate_chat_response(message, temperature, city, preferences=None):
    """Generate a contextual chat response based on message, weather, and preferences"""
    message_lower = message.lower()
    
    # Get style preference for personalization
    style = 'casual'
    if preferences and preferences.get('style'):
        style = preferences['style'][0].lower() if isinstance(preferences['style'], list) else preferences['style'].lower()
    
    # Activity-based responses
    if 'hiking' in message_lower or 'trail' in message_lower or 'camping' in message_lower:
        return f"For hiking in {city}, I recommend moisture-wicking layers, sturdy trail boots, a backpack, water bottle, trail hat, and bug spray. Don't forget energy snacks!"
    
    elif 'beach' in message_lower or 'pool' in message_lower or 'swim' in message_lower:
        return "For the beach, pack swimwear, a light cover-up, flip-flops, beach hat, SPF 50+ waterproof sunscreen, sunglasses, a beach towel, and a waterproof bag!"
    
    elif 'formal' in message_lower:
        if temperature < 50:
            return f"For formal occasions in {city} ({temperature}°F), wear a wool suit, button shirt with knit sweater underneath, thick overcoat, warm scarf, leather gloves, and dress shoes with warm socks."
        elif 'rain' in message_lower or 'rain' in city.lower():
            return "For formal events in rainy weather, I recommend a water-resistant coat, waterproof dress shoes, compact umbrella, quick-dry dress pants, button shirt, and a smooth-finish blazer."
        elif temperature > 70:
            return f"For formal occasions in warm weather ({temperature}°F), choose a light-colored linen or cotton suit, breathable cotton shirt, light blazer, polarized sunglasses, and dress shoes with breathable socks."
        else:
            return f"For formal occasions ({temperature}°F), I suggest a lightweight breathable suit, cotton button shirt, moisture-wicking undershirt, light blazer, and dress shoes with thin socks."
    
    elif 'travel' in message_lower or 'flight' in message_lower or 'airport' in message_lower:
        return "For travel, wear comfortable layers, stretch pants, slip-on shoes for security, and bring a neck pillow, eye mask, compact toiletries, water bottle, and document holder!"
    
    elif 'sport' in message_lower or 'exercise' in message_lower or 'gym' in message_lower or 'workout' in message_lower:
        return "For sports, wear moisture-wicking athletic shirt, flexible shorts or pants, activity-specific shoes, sports visor, sweatband, and bring a hydration bottle!"
    
    elif 'commute' in message_lower or 'work' in message_lower or 'office' in message_lower:
        return f"For commuting in {city}, wear comfortable walking shoes, weather-appropriate layers, bring a light bag, compact umbrella, phone charger, and reusable bottle!"
    
    # Weather-based responses
    elif 'tomorrow' in message_lower:
        return f"Tomorrow in {city}, expect light rain with a high of 58°F. I'd recommend a waterproof jacket, quick-dry pants, and water-resistant shoes."
    
    elif 'cold' in message_lower or 'colder' in message_lower:
        return "If it gets colder, add a warm sweater or thermal layer. Below 45°F, bring a scarf and gloves. Below 32°F, you'll need a thick insulated jacket!"
    
    elif 'rain' in message_lower:
        return "For rainy weather, I recommend a waterproof jacket with hood, quick-dry pants, water-resistant shoes, an umbrella, and a backpack rain cover!"
    
    elif 'snow' in message_lower:
        return "For snowy weather, wear an insulated coat, thermal layers, snow pants, snow boots, waterproof gloves, warm hat, face covering, and snow goggles if windy!"
    
    elif 'jacket' in message_lower:
        if temperature < 60:
            return "Of course. A wind-resistant jacket or warm fleece would work well today."
        else:
            return "It's warm today, so a light cardigan or windbreaker would be perfect if you prefer an extra layer."
    
    else:
        # General response based on temperature and style
        if temperature < 50:
            return f"Based on the current {temperature}°F in {city}, I recommend layering with a jacket, long sleeves, and comfortable pants. Your {style} style will look great with these layers!"
        elif temperature < 70:
            return f"The weather in {city} is pleasant at {temperature}°F. Perfect for your {style} style - a light jacket, comfortable shirt, and jeans would work perfectly!"
        else:
            return f"It's warm in {city} at {temperature}°F! Light, breathable clothing like shorts and a cotton shirt would be ideal for your {style} style."


@app.route('/')
def index():
    """Serve the main chat interface"""
    response = make_response(render_template('index.html'))
    # Prevent browser caching to ensure icon updates are always visible
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/icon-test')
def icon_test():
    """Weather icon test page"""
    return render_template('icon_test.html')


@app.route('/api/weather', methods=['GET'])
def weather():
    """Get current weather data for a city with caching"""
    try:
        city = request.args.get('city', 'Redmond')
        
        logger.info(f"Weather request for city: {city}")
        
        # Check cache first
        cached_data = get_cached_weather(city)
        if cached_data:
            return jsonify(cached_data)
        
        # Fetch real weather data
        weather_data = get_current_weather(city)
        
        # Add UV index (not in current data)
        weather_data['uv_index'] = 5
        
        # Cache the data
        cache_weather_data(city, weather_data)
        
        logger.info(f"Weather response - City: {city}, Temp: {weather_data.get('temperature')}°F")
        
        return jsonify(weather_data)
        
    except Exception as e:
        logger.error(f"Weather error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/outfit', methods=['GET'])
def outfit():
    """Get outfit suggestions based on weather and preferences (reuses weather data from client)"""
    try:
        city = request.args.get('city', 'San Francisco')
        
        # Check if weather data was passed to avoid redundant API call
        temp = request.args.get('temperature', type=float)
        condition = request.args.get('condition', '')
        
        # Get user preferences
        style = request.args.get('style', 'Casual').split(',')
        clothing_types = request.args.get('types', 'Jackets,Jeans,Sneakers').split(',')
        colors = request.args.get('colors', 'Neutral,Blues').split(',')
        
        logger.info(f"Outfit request for city: {city}, style: {style}")
        
        # Only fetch weather if not provided (fallback)
        if temp is None or not condition:
            logger.info("Weather data not provided, fetching from API")
            weather_data = get_current_weather(city)
            temp = weather_data.get('temperature', 65)
            condition = weather_data.get('condition', 'partly cloudy')
        else:
            logger.info(f"Reusing weather data: {temp}°F, {condition}")
        
        # Generate outfit based on temperature, condition, and preferences
        # Check if activity is specified in request
        activity = request.args.get('activity', None)
        items = generate_comprehensive_outfit(temp, condition, style, clothing_types, colors, activity)
        
        return jsonify({
            'city': city,
            'temperature': temp,
            'items': items
        })
        
    except Exception as e:
        logger.error(f"Outfit error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with preference awareness - Routes to Coach Agent if available"""
    try:
        data = request.json
        message = data.get('message', '')
        city = data.get('city', 'Redmond')
        preferences = data.get('preferences', {})
        session_id = data.get('session_id', 'default')
        user_id = data.get('user_id', 'anonymous')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Chat request - Session: {session_id}, City: {city}, Message: {message[:50]}...")
        
        # Track metrics
        with agent_metrics.measure_time("chat_request", labels={"endpoint": "chat"}):
            try:
                # Try to use ADK Coach Agent first
                agent_response = call_coach_agent(
                    message=f"{message} (City: {city})",
                    user_id=user_id,
                    session_id=session_id
                )
                
                if agent_response:
                    # Successfully got response from Coach Agent
                    logger.info("✅ Using Coach Agent response (A2A protocol)")
                    response_text = agent_response.get('response', agent_response.get('message', ''))
                    
                    # Track success
                    agent_metrics.increment_counter(
                        "chat_requests",
                        labels={"endpoint": "chat", "source": "adk_agent", "status": "success"}
                    )
                    
                    return jsonify({
                        'response': response_text,
                        'source': 'adk_coach_agent'
                    })
                
                # Fallback to direct functions if Coach Agent unavailable
                logger.info("⚠️ Falling back to direct functions")
                
                # Get weather context for better responses
                weather_data = get_current_weather(city)
                temp = weather_data.get('temperature', 65)
                condition = weather_data.get('condition', 'partly cloudy')
                
                # Generate contextual response with preferences
                response_text = generate_chat_response(message, temp, city, preferences)
                
                # Track success (fallback mode)
                agent_metrics.increment_counter(
                    "chat_requests",
                    labels={"endpoint": "chat", "source": "fallback", "status": "success"}
                )
                
                logger.info(f"Chat response - Session: {session_id}, Length: {len(response_text)}")
                
                return jsonify({
                    'response': response_text,
                    'session_id': session_id
                })
                
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                agent_metrics.increment_counter(
                    "chat_requests",
                    labels={"endpoint": "chat", "status": "error"}
                )
                return jsonify({
                    'error': f'Error: {str(e)}'
                }), 500
        
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'frontend'}), 200


@app.route('/api/metrics')
def metrics():
    """Get current metrics statistics"""
    stats = agent_metrics.get_stats()
    return jsonify(stats)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
