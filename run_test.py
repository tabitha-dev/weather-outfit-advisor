"""Simple test to verify the multi-agent system works."""

print("🚀 Weather Outfit ADK - Quick Test")
print("=" * 60)

try:
    from weather_outfit_adk.tools import get_current_weather, classify_activity, plan_outfit, check_safety
    print("✅ Tools imported successfully")
    
    print("\n📦 Testing Weather Tool (with mock data)...")
    weather = get_current_weather("Seattle")
    print(f"   Temperature: {weather['temperature']}°F")
    print(f"   Condition: {weather['condition']}")
    print(f"   Rain chance: {weather['rain_chance']}%")
    
    print("\n📦 Testing Activity Classification...")
    activity = classify_activity("going hiking this afternoon")
    print(f"   Category: {activity['category']}")
    print(f"   Formality: {activity['formality_level']}")
    print(f"   Movement: {activity['movement_level']}")
    
    print("\n📦 Testing Outfit Planning...")
    outfit = plan_outfit(
        temperature=58.0,
        rain_chance=40.0,
        wind_speed=12.0,
        activity_category="sports",
        formality_level="casual",
        movement_level="high",
        persona="practical"
    )
    print(f"   Top: {outfit['top']}")
    print(f"   Bottom: {outfit['bottom']}")
    print(f"   Outer: {outfit['outer_layer']}")
    print(f"   Shoes: {outfit['footwear']}")
    print(f"   Notes: {outfit['notes']}")
    
    print("\n📦 Testing Safety Check...")
    safety = check_safety(temperature=18.0, wind_speed=25.0, rain_chance=10.0)
    print(f"   Risk level: {safety['risk_level']}")
    if safety['safety_message']:
        print(f"   Warning: {safety['safety_message']}")
    
    print("\n" + "=" * 60)
    print("✅ All basic tests passed!")
    print("=" * 60)
    print("\nℹ️  To test the full agent system:")
    print("   python app.py")
    print("\nℹ️  To run comprehensive tests:")
    print("   python test_local.py")
    print("\nℹ️  Note: Using mock weather data")
    print("   Set WEATHER_API_KEY for real data")
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
