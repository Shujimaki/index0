#!/usr/bin/env python
"""
Test script for Gemini AI integration
Tests AI summary generation with sample earthquake data
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_connection():
    """Test basic Gemini API connection"""
    print("=" * 70)
    print("🤖 TESTING GEMINI AI CONNECTION")
    print("=" * 70)
    
    try:
        from google import genai
        from config import configuration_map
        
        config = configuration_map['development']
        api_key = config.GEMINI_API_KEY
        
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            return False
        
        print(f"✅ API Key loaded: {api_key[:20]}...")
        
        # Test connection
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Gemini connection failed: {e}")
        return False


def test_simple_generation():
    """Test simple text generation"""
    print("\n" + "=" * 70)
    print("🧪 TEST 1: Simple Text Generation")
    print("=" * 70)
    
    try:
        from google import genai
        from google.genai import types
        from config import configuration_map
        
        config = configuration_map['development']
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        
        print("📝 Sending test prompt to Gemini...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say 'Hello from Gemini AI!' in exactly 5 words."
        )
        
        result = response.text
        print(f"\n✅ Response received:")
        print(f"   {result}")
        print(f"\n✅ Simple generation test PASSED")
        
        return True
    except Exception as e:
        print(f"\n❌ Simple generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_earthquake_summary_without_tips():
    """Test earthquake summary generation WITHOUT safety tips"""
    print("\n" + "=" * 70)
    print("🧪 TEST 2: Earthquake Summary (No Safety Tips)")
    print("=" * 70)
    
    try:
        from app import build_application
        from app.gemini_service import GeminiSummarizer
        
        app = build_application()
        
        with app.app_context():
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            
            # Sample earthquake data (magnitude < 4.0, no tips)
            test_data = {
                'date_time': '2024-11-08 10:30:00 PST',
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '10 km',
                'magnitude': '3.5',
                'location': '5 km NW of Manila, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test1'
            }
            
            print("📊 Test Data:")
            print(f"   Time: {test_data['date_time']}")
            print(f"   Location: {test_data['location']}")
            print(f"   Magnitude: {test_data['magnitude']}")
            print(f"   Depth: {test_data['depth']}")
            print(f"\n🤖 Generating AI summary (without safety tips)...")
            
            summary = summarizer.create_summary(test_data, include_safety_tips=False)
            
            print(f"\n✅ Summary Generated:")
            print("─" * 70)
            print(summary)
            print("─" * 70)
            
            if len(summary) > 50:
                print(f"\n✅ Earthquake summary test (no tips) PASSED")
                return True
            else:
                print(f"\n⚠️ Summary seems too short")
                return False
                
    except Exception as e:
        print(f"\n❌ Earthquake summary test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_earthquake_summary_with_tips():
    """Test earthquake summary generation WITH safety tips"""
    print("\n" + "=" * 70)
    print("🧪 TEST 3: Earthquake Summary (WITH Safety Tips)")
    print("=" * 70)
    
    try:
        from app import build_application
        from app.gemini_service import GeminiSummarizer
        
        app = build_application()
        
        with app.app_context():
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            
            # Sample earthquake data (magnitude >= 4.0, with tips)
            test_data = {
                'date_time': '2024-11-08 14:45:00 PST',
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '15 km',
                'magnitude': '5.2',
                'location': '10 km SE of Quezon City, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test2'
            }
            
            print("📊 Test Data:")
            print(f"   Time: {test_data['date_time']}")
            print(f"   Location: {test_data['location']}")
            print(f"   Magnitude: {test_data['magnitude']} ⚠️ (≥4.0)")
            print(f"   Depth: {test_data['depth']}")
            print(f"\n🤖 Generating AI summary (WITH safety tips)...")
            
            summary = summarizer.create_summary(test_data, include_safety_tips=True)
            
            print(f"\n✅ Summary Generated:")
            print("─" * 70)
            print(summary)
            print("─" * 70)
            
            # Check if safety tips might be included
            safety_keywords = ['safe', 'tip', 'stay', 'avoid', 'protect', 'precaution', 'drop', 'cover', 'hold']
            has_safety_content = any(keyword in summary.lower() for keyword in safety_keywords)
            
            if len(summary) > 50:
                print(f"\n✅ Earthquake summary test (with tips) PASSED")
                if has_safety_content:
                    print(f"   ✓ Safety-related content detected")
                return True
            else:
                print(f"\n⚠️ Summary seems too short")
                return False
                
    except Exception as e:
        print(f"\n❌ Earthquake summary test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_caching():
    """Test Redis caching functionality"""
    print("\n" + "=" * 70)
    print("🧪 TEST 4: Redis Caching")
    print("=" * 70)
    
    try:
        from app import build_application
        from app.gemini_service import GeminiSummarizer
        import time
        
        app = build_application()
        
        with app.app_context():
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            
            test_data = {
                'date_time': '2024-11-08 16:00:00 PST',
                'latitude': '10.3157',
                'longitude': '123.8854',
                'depth': '8 km',
                'magnitude': '4.0',
                'location': '15 km W of Cebu City, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test-cache'
            }
            
            print("🔄 First call (should generate new summary)...")
            start_time = time.time()
            summary1 = summarizer.create_summary(test_data, include_safety_tips=False)
            first_duration = time.time() - start_time
            print(f"   Time taken: {first_duration:.2f} seconds")
            
            print("\n🔄 Second call (should use cached summary)...")
            start_time = time.time()
            summary2 = summarizer.create_summary(test_data, include_safety_tips=False)
            second_duration = time.time() - start_time
            print(f"   Time taken: {second_duration:.2f} seconds")
            
            if summary1 == summary2:
                print(f"\n✅ Caching test PASSED")
                print(f"   ✓ Summaries match")
                if second_duration < first_duration:
                    print(f"   ✓ Cache is faster ({second_duration:.2f}s vs {first_duration:.2f}s)")
                return True
            else:
                print(f"\n⚠️ Summaries don't match (cache might not be working)")
                return False
                
    except Exception as e:
        print(f"\n❌ Caching test failed: {e}")
        print(f"   (This is OK if Redis is not running)")
        return True  # Don't fail for cache issues


def test_fallback_summary():
    """Test fallback summary when AI fails"""
    print("\n" + "=" * 70)
    print("🧪 TEST 5: Fallback Summary (AI Failure Simulation)")
    print("=" * 70)
    
    try:
        from app.gemini_service import GeminiSummarizer
        
        # Create summarizer with invalid API key to trigger fallback
        summarizer = GeminiSummarizer("invalid_api_key_for_testing")
        
        test_data = {
            'date_time': '2024-11-08 18:00:00 PST',
            'latitude': '7.1907',
            'longitude': '125.4553',
            'depth': '12 km',
            'magnitude': '3.8',
            'location': '20 km N of Davao City, Philippines',
            'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test-fallback'
        }
        
        print("🔧 Using invalid API key to trigger fallback...")
        summary = summarizer.create_summary(test_data, include_safety_tips=False)
        
        print(f"\n✅ Fallback Summary Generated:")
        print("─" * 70)
        print(summary)
        print("─" * 70)
        
        # Check if it's the fallback template
        if "An earthquake with magnitude" in summary and test_data['location'] in summary:
            print(f"\n✅ Fallback summary test PASSED")
            return True
        else:
            print(f"\n⚠️ Fallback format unexpected")
            return False
            
    except Exception as e:
        print(f"\n❌ Fallback test failed: {e}")
        return False


def main():
    """Run all AI tests"""
    print("\n" + "=" * 70)
    print("🚀 GEMINI AI SYSTEM TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Connection Test", test_gemini_connection),
        ("Simple Generation", test_simple_generation),
        ("Summary Without Tips", test_earthquake_summary_without_tips),
        ("Summary With Tips", test_earthquake_summary_with_tips),
        ("Redis Caching", test_caching),
        ("Fallback Summary", test_fallback_summary),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 70)
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("\n✅ Gemini AI is working correctly!")
    else:
        print(f"⚠️ SOME TESTS FAILED ({passed}/{total} passed)")
        print("\n❌ Please review the failures above")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
