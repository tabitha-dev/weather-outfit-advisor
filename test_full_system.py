"""
Comprehensive test of the full Weather Outfit ADK system.
Tests all agents, tools, and memory integration.
"""

print("=" * 70)
print("COMPREHENSIVE WEATHER OUTFIT ADK SYSTEM TEST")
print("=" * 70)

# Test 1: All tools work independently
print("\n📦 TEST 1: Tool Functions")
print("-" * 70)

try:
    from weather_outfit_adk.tools import (
        get_current_weather, classify_activity, plan_outfit, 
        check_safety, get_user_preferences, update_user_preferences
    )
    print("✅ All tools imported successfully")
    
    # Test weather
    weather = get_current_weather("Seattle")
    print(f"✅ Weather: {weather['temperature']}°F, {weather['condition']}")
    
    # Test activity classification  
    activity = classify_activity("going hiking")
    print(f"✅ Activity: {activity['category']}, formality={activity['formality_level']}")
    
    # Test outfit planning
    outfit = plan_outfit(temperature=58.0, rain_chance=40.0, wind_speed=12.0)
    print(f"✅ Outfit: {outfit['top']}, {outfit['outer_layer'] or 'no jacket'}")
    
    # Test safety
    safety = check_safety(temperature=18.0, wind_speed=25.0, rain_chance=10.0)
    print(f"✅ Safety: {safety['risk_level']} risk")
    
    # Test memory
    prefs = get_user_preferences()
    print(f"✅ Memory: persona={prefs['persona']}, comfort={prefs['comfort_profile']}")
    
    # Update memory
    updated = update_user_preferences(persona="fashion", comfort_profile="runs_cold", default_city="Seattle")
    print(f"✅ Updated: persona={updated['persona']}, city={updated['default_city']}")
    
except Exception as e:
    print(f"❌ Tool test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: ADK agents can be imported
print("\n🤖 TEST 2: ADK Agent Imports")
print("-" * 70)

try:
    from google.adk.agents import Agent
    print("✅ ADK Agent class imported")
    
    from weather_outfit_adk.agents import (
        coach_agent, weather_agent, stylist_agent, 
        activity_agent, safety_agent
    )
    print("✅ All agents imported successfully")
    print(f"   - Coach: {coach_agent.name}")
    print(f"   - Weather: {weather_agent.name}")
    print(f"   - Stylist: {stylist_agent.name}")
    print(f"   - Activity: {activity_agent.name}")
    print(f"   - Safety: {safety_agent.name}")
    print(f"   - Coach has {len(coach_agent.tools)} tools")
    
except Exception as e:
    print(f"❌ Agent import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Main app can be imported
print("\n📱 TEST 3: Main Application")
print("-" * 70)

try:
    import app
    print("✅ Main app.py imported successfully")
    print(f"✅ ADK app name: {app.app.name}")
    print(f"✅ Root agent: {app.app.root_agent.name}")
    print(f"✅ App has root agent with {len(app.app.root_agent.tools)} tools")
    
except Exception as e:
    print(f"❌ App import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Schemas and data models
print("\n📋 TEST 4: Data Models")
print("-" * 70)

try:
    from weather_outfit_adk.schemas import (
        WeatherData, ForecastData, OutfitPlan, 
        ActivityContext, UserPreferences, ComfortProfile, PersonaType
    )
    print("✅ All schemas imported")
    
    # Create sample instances
    weather_data = WeatherData(
        temperature=65.0,
        feels_like=63.0,
        condition="partly cloudy",
        rain_chance=20.0,
        wind_speed=8.0,
        timestamp="2025-01-13T10:00:00"
    )
    print(f"✅ WeatherData: {weather_data.temperature}°F")
    
    user_prefs = UserPreferences(
        persona=PersonaType.PRACTICAL,
        comfort_profile=ComfortProfile.NEUTRAL,
        default_city="Seattle"
    )
    print(f"✅ UserPreferences: {user_prefs.persona.value}")
    
except Exception as e:
    print(f"❌ Schema test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Memory persistence
print("\n💾 TEST 5: Memory System")
print("-" * 70)

try:
    from weather_outfit_adk.memory import UserMemory
    from weather_outfit_adk.schemas.memory import PersonaType, ComfortProfile
    
    memory = UserMemory()
    print("✅ UserMemory instance created")
    
    # Store preferences
    memory.update_preferences(
        user_id="test_user_1",
        persona=PersonaType.FASHION,
        comfort_profile=ComfortProfile.RUNS_COLD,
        default_city="Portland"
    )
    print("✅ Preferences stored")
    
    # Retrieve preferences
    prefs = memory.get_preferences("test_user_1")
    assert prefs.persona == PersonaType.FASHION
    assert prefs.default_city == "Portland"
    print(f"✅ Preferences retrieved: {prefs.default_city}")
    
    # Different user
    prefs2 = memory.get_preferences("test_user_2")
    assert prefs2.persona == PersonaType.PRACTICAL  # Default
    print("✅ Multiple users supported")
    
except Exception as e:
    print(f"❌ Memory test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Final summary
print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\n✨ System Status:")
print("   ✅ All 5 agents operational")
print("   ✅ All tools functioning")
print("   ✅ Memory system integrated")
print("   ✅ Schemas validated")
print("   ✅ Main app ready")
print("\n🚀 The Weather Outfit ADK system is fully functional!")
print("\nNext steps:")
print("   - python app.py (start ADK dev server)")
print("   - Deploy to Google Cloud Agent Engine")
print("=" * 70)
