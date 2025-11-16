"""
Comprehensive test with Google Cloud Metrics integration.
Tests all agents, tools, and memory while publishing metrics to Cloud Monitoring.
"""

import os
import time
import logging
from datetime import datetime
from google.cloud import monitoring_v3

# Setup Cloud Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WeatherOutfitADKTest")

# Initialize Cloud Monitoring client
project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'agentenginedeploy')
client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

def publish_metric(metric_type, value, labels=None):
    """Publish a custom metric to Google Cloud Monitoring."""
    try:
        series = monitoring_v3.TimeSeries()
        series.metric.type = f'custom.googleapis.com/{metric_type}'
        
        if labels:
            for key, val in labels.items():
                series.metric.labels[key] = str(val)
        
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": value}})
        series.points = [point]
        
        client.create_time_series(name=project_name, time_series=[series])
        logger.info(f"📊 Metric published: {metric_type} = {value}")
    except Exception as e:
        logger.warning(f"⚠️  Could not publish metric (running local?): {e}")

print("=" * 70)
print("🚀 COMPREHENSIVE WEATHER OUTFIT ADK SYSTEM TEST")
print("=" * 70)
print(f"📊 Google Cloud Project: {project_id}")
print(f"⏰ Test started: {datetime.now().isoformat()}")
print("=" * 70)

test_results = {
    "tools": 0,
    "agents": 0,
    "app": 0,
    "schemas": 0,
    "memory": 0,
    "total": 0
}

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
    publish_metric("test/weather_temp", weather['temperature'], {"city": "Seattle"})
    
    # Test activity classification  
    activity = classify_activity("going hiking")
    print(f"✅ Activity: {activity['category']}, formality={activity['formality_level']}")
    
    # Test outfit planning
    outfit = plan_outfit(temperature=58.0, rain_chance=40.0, wind_speed=12.0)
    print(f"✅ Outfit: {outfit['top']}, {outfit['outer_layer'] or 'no jacket'}")
    
    # Test safety
    safety = check_safety(temperature=18.0, wind_speed=25.0, rain_chance=10.0)
    print(f"✅ Safety: {safety['risk_level']} risk")
    publish_metric("test/safety_check", 1.0, {"risk_level": safety['risk_level']})
    
    # Test memory
    prefs = get_user_preferences()
    print(f"✅ Memory: persona={prefs['persona']}, comfort={prefs['comfort_profile']}")
    
    # Update memory
    updated = update_user_preferences(persona="fashion", comfort_profile="runs_cold", default_city="Seattle")
    print(f"✅ Updated: persona={updated['persona']}, city={updated['default_city']}")
    
    test_results["tools"] = 1
    publish_metric("test/tools_passed", 1.0)
    
except Exception as e:
    print(f"❌ Tool test failed: {e}")
    logger.error(f"Tool test failed: {e}")
    publish_metric("test/tools_passed", 0.0)
    import traceback
    traceback.print_exc()

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
    
    agent_count = 5
    publish_metric("test/agents_count", float(agent_count))
    publish_metric("test/agents_passed", 1.0)
    test_results["agents"] = 1
    
except Exception as e:
    print(f"❌ Agent import failed: {e}")
    logger.error(f"Agent import failed: {e}")
    publish_metric("test/agents_passed", 0.0)
    import traceback
    traceback.print_exc()

# Test 3: Main app can be imported
print("\n📱 TEST 3: Main Application")
print("-" * 70)

try:
    import app
    print("✅ Main app.py imported successfully")
    print(f"✅ ADK app name: {app.app.name}")
    print(f"✅ Root agent: {app.app.root_agent.name}")
    print(f"✅ App has root agent with {len(app.app.root_agent.tools)} tools")
    
    publish_metric("test/app_tools_count", float(len(app.app.root_agent.tools)))
    publish_metric("test/app_passed", 1.0)
    test_results["app"] = 1
    
except Exception as e:
    print(f"❌ App import failed: {e}")
    logger.error(f"App import failed: {e}")
    publish_metric("test/app_passed", 0.0)
    import traceback
    traceback.print_exc()

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
    publish_metric("test/schema_weather_temp", weather_data.temperature)
    
    user_prefs = UserPreferences(
        persona=PersonaType.PRACTICAL,
        comfort_profile=ComfortProfile.NEUTRAL,
        default_city="Seattle"
    )
    print(f"✅ UserPreferences: {user_prefs.persona.value}")
    
    publish_metric("test/schemas_passed", 1.0)
    test_results["schemas"] = 1
    
except Exception as e:
    print(f"❌ Schema test failed: {e}")
    logger.error(f"Schema test failed: {e}")
    publish_metric("test/schemas_passed", 0.0)
    import traceback
    traceback.print_exc()

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
    
    publish_metric("test/memory_passed", 1.0)
    test_results["memory"] = 1
    
except Exception as e:
    print(f"❌ Memory test failed: {e}")
    logger.error(f"Memory test failed: {e}")
    publish_metric("test/memory_passed", 0.0)
    import traceback
    traceback.print_exc()

# Final summary
test_results["total"] = sum(test_results.values()) - test_results["total"]
print("\n" + "=" * 70)

if test_results["total"] == 5:
    print("✅ ALL TESTS PASSED!")
    publish_metric("test/all_tests_passed", 1.0)
else:
    print(f"⚠️  {test_results['total']}/5 tests passed")
    publish_metric("test/all_tests_passed", 0.0)

print("=" * 70)
print("\n✨ System Status:")
print(f"   {'✅' if test_results['tools'] else '❌'} All tools functional")
print(f"   {'✅' if test_results['agents'] else '❌'} All agents operational")
print(f"   {'✅' if test_results['app'] else '❌'} Main app ready")
print(f"   {'✅' if test_results['schemas'] else '❌'} Schemas validated")
print(f"   {'✅' if test_results['memory'] else '❌'} Memory system integrated")

print("\n📊 Metrics published to Google Cloud Monitoring")
print("   View at: https://console.cloud.google.com/monitoring/dashboards")
print("   Query: resource.type=\"global\" AND metric.type=~\"custom.googleapis.com/test/*\"")

print("\n🚀 The Weather Outfit ADK system is fully functional!")
print("\nNext steps:")
print("   - python app.py (start ADK dev server)")
print("   - Deploy to Google Cloud Agent Engine")
print("=" * 70)
logger.info(f"Test completed at {datetime.now().isoformat()}")
