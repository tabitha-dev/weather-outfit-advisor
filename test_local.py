"""
Local test runner for Weather Outfit ADK
Tests the multi-agent system locally before deployment
"""

import os
from dotenv import load_dotenv

load_dotenv()

from weather_outfit_adk.agents import coach_agent, weather_agent, stylist_agent, activity_agent, safety_agent
from weather_outfit_adk.memory import UserMemory
from weather_outfit_adk.schemas.memory import PersonaType, ComfortProfile

memory = UserMemory()

def test_weather_agent():
    """Test Weather agent standalone."""
    print("\n" + "="*60)
    print("Testing Weather Agent")
    print("="*60)
    
    result = weather_agent.generate_content("What's the weather in Seattle?")
    print(f"Weather Agent Response: {result}")
    return result

def test_activity_agent():
    """Test Activity agent standalone."""
    print("\n" + "="*60)
    print("Testing Activity Agent")
    print("="*60)
    
    result = activity_agent.generate_content("I'm going hiking this afternoon")
    print(f"Activity Agent Response: {result}")
    return result

def test_safety_agent():
    """Test Safety agent standalone."""
    print("\n" + "="*60)
    print("Testing Safety Agent")
    print("="*60)
    
    result = safety_agent.generate_content("Check safety for temperature 18F, wind 25 mph, rain 10%")
    print(f"Safety Agent Response: {result}")
    return result

def test_stylist_agent():
    """Test Stylist agent standalone."""
    print("\n" + "="*60)
    print("Testing Stylist Agent")
    print("="*60)
    
    result = stylist_agent.generate_content(
        "Recommend outfit for 58F, 40% rain, 12 mph wind, casual activity, practical persona"
    )
    print(f"Stylist Agent Response: {result}")
    return result

def test_coach_full_flow():
    """Test Coach agent with full multi-agent flow."""
    print("\n" + "="*60)
    print("Testing Coach Agent (Full Flow)")
    print("="*60)
    
    test_queries = [
        "What should I wear today in Seattle?",
        "I'm going hiking this afternoon in Portland",
        "What should I wear for a business meeting in Boston?",
        "I'm taking my kid to school in Chicago",
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 60)
        result = coach_agent.generate_content(query)
        print(f"🤖 Response: {result}")
        print("-" * 60)

def test_memory_system():
    """Test memory and preference system."""
    print("\n" + "="*60)
    print("Testing Memory System")
    print("="*60)
    
    user_id = "test_user_123"
    
    memory.update_preferences(
        user_id=user_id,
        persona=PersonaType.FASHION,
        comfort_profile=ComfortProfile.RUNS_COLD,
        default_city="Seattle"
    )
    
    prefs = memory.get_preferences(user_id)
    print(f"Stored Preferences: {prefs.dict()}")
    
    print("\nTesting with persona preference...")
    result = coach_agent.generate_content(
        f"What should I wear in {prefs.default_city}? (User prefers {prefs.persona.value} style and {prefs.comfort_profile.value})"
    )
    print(f"Response: {result}")

def run_all_tests():
    """Run all tests."""
    print("\n🚀 Starting Weather Outfit ADK Tests")
    print("="*60)
    
    try:
        test_weather_agent()
        test_activity_agent()
        test_safety_agent()
        test_stylist_agent()
        test_memory_system()
        test_coach_full_flow()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
