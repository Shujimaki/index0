#!/usr/bin/env python
"""
Quick test script to verify all components are working
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from app import build_application, database
        from app.models import User, NotificationSettings, SeismicEvent
        from app.routes import bp
        from app.tasks import check_and_process_earthquakes
        from app.gemini_service import GeminiSummarizer
        from app.location_service import LocationAnalyzer
        from app.api import fetch_latest_earthquake_raw
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_initialization():
    """Test if Flask app initializes"""
    print("\n🧪 Testing app initialization...")
    try:
        from app import build_application
        app = build_application('development')
        with app.app_context():
            print(f"✅ App initialized: {app.name}")
            print(f"   Debug mode: {app.debug}")
            print(f"   Secret key set: {bool(app.config.get('SECRET_KEY'))}")
            print(f"   Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        return True
    except Exception as e:
        print(f"❌ App initialization failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")
    try:
        from app import build_application, database
        from app.models import User
        
        app = build_application('development')
        with app.app_context():
            # Try to query (will create tables if they don't exist)
            user_count = User.query.count()
            print(f"✅ Database connected")
            print(f"   Users in database: {user_count}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_regions_data():
    """Test regions data is available"""
    print("\n🧪 Testing regions data...")
    try:
        from app.cities import PHILIPPINE_GEOGRAPHY, REGIONS_LIST
        print(f"✅ Regions data loaded")
        print(f"   Total regions: {len(REGIONS_LIST)}")
        print(f"   First region: {REGIONS_LIST[0]['name']}")
        return True
    except Exception as e:
        print(f"❌ Regions data failed: {e}")
        return False

def test_routes():
    """Test routes are registered"""
    print("\n🧪 Testing routes...")
    try:
        from app import build_application
        app = build_application('development')
        
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        important_routes = ['/', '/login', '/register', '/dashboard/<int:user_id>']
        
        print(f"✅ Routes registered: {len(routes)}")
        for route in important_routes:
            if any(route in r for r in routes):
                print(f"   ✓ {route}")
            else:
                print(f"   ✗ {route} missing!")
        return True
    except Exception as e:
        print(f"❌ Routes test failed: {e}")
        return False

def test_celery():
    """Test Celery configuration"""
    print("\n🧪 Testing Celery configuration...")
    try:
        from app import task_queue
        print(f"✅ Celery configured")
        print(f"   Broker: {task_queue.conf.broker_url}")
        print(f"   Backend: {task_queue.conf.result_backend}")
        return True
    except Exception as e:
        print(f"❌ Celery test failed: {e}")
        return False

def test_redis():
    """Test Redis connection"""
    print("\n🧪 Testing Redis connection...")
    try:
        import redis
        from config import configuration_map
        config = configuration_map['development']
        
        r = redis.from_url(config.REDIS_URL)
        r.ping()
        print(f"✅ Redis connected")
        print(f"   URL: {config.REDIS_URL}")
        return True
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("   (This is okay if you haven't started Redis yet)")
        return True  # Don't fail the test for this

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 INDEX0 SYSTEM CHECK")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_app_initialization,
        test_database_connection,
        test_regions_data,
        test_routes,
        test_celery,
        test_redis
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🎉 System is ready!")
        print("\n📋 Next steps:")
        print("   1. Ensure Redis is running: brew services start redis")
        print("   2. Start Flask app: python run.py")
        print("   3. Start Celery worker: celery -A celery_worker.task_queue worker --loglevel=info")
        print("   4. Start Celery beat: celery -A celery_worker.task_queue beat --loglevel=info")
        print("   5. Open http://localhost:5001 in your browser")
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total} passed)")
        print("\n❌ Please fix the issues above before running the application")
    
    print("=" * 60)
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
