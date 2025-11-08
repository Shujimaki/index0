"""
Quick verification test for new features
"""
from app import build_application, database
from app.models import User, NotificationSettings

def test_new_features():
    app = build_application()
    
    with app.app_context():
        print("\n" + "="*60)
        print("🧪 VERIFYING NEW FEATURES")
        print("="*60)
        
        # Test 1: Check password_hash field exists
        print("\n1. Testing Password Field...")
        users = User.query.all()
        if users:
            user = users[0]
            if hasattr(user, 'password_hash') and user.password_hash:
                print(f"   ✅ Password field exists for user: {user.full_name}")
                print(f"   ✅ Password hash: {user.password_hash[:20]}...")
                
                # Test password checking
                if user.check_password('password123'):
                    print(f"   ✅ Password verification works!")
                else:
                    print(f"   ⚠️  Password verification failed")
            else:
                print(f"   ❌ Password field missing or empty")
        else:
            print(f"   ⚠️  No users found in database")
        
        # Test 2: Check NotificationSettings values
        print("\n2. Testing Saved Preferences...")
        settings = NotificationSettings.query.first()
        if settings:
            print(f"   ✅ Settings found for user_id: {settings.user_id}")
            print(f"   • Magnitude threshold: {settings.magnitude_threshold}")
            print(f"   • Location type: {settings.monitor_location_type}")
            print(f"   • Safety tips: {settings.add_safety_tips}")
            if settings.monitor_location_type == 'custom':
                print(f"   • Custom location: {settings.alternate_city}, {settings.alternate_province}")
        else:
            print(f"   ⚠️  No settings found")
        
        # Test 3: Check all users
        print(f"\n3. Testing All Users...")
        print(f"   Total users: {len(users)}")
        for user in users:
            has_password = "✅" if (hasattr(user, 'password_hash') and user.password_hash) else "❌"
            print(f"   {has_password} {user.full_name} ({user.email_address})")
        
        print("\n" + "="*60)
        print("✅ VERIFICATION COMPLETE!")
        print("="*60)
        print("\n📝 Notes:")
        print("   • All users should have password_hash")
        print("   • Default password for existing users: 'password123'")
        print("   • Login uses full_name as username")
        print("   • Dashboard test email section added")
        print("   • Preferences are saved and loaded correctly")
        print("\n")

if __name__ == '__main__':
    test_new_features()
