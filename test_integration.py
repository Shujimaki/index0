#!/usr/bin/env python
"""
Integration test - Tests both AI and Email together
Simulates the complete notification flow
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_notification_flow():
    """Test the complete notification flow from earthquake data to email"""
    print("=" * 70)
    print("🚀 COMPLETE NOTIFICATION FLOW TEST")
    print("=" * 70)
    
    try:
        from app import build_application, email_service, database
        from flask_mail import Message
        from app.gemini_service import GeminiSummarizer
        from app.location_service import LocationAnalyzer
        from app.models import User, NotificationSettings
        
        app = build_application()
        
        with app.app_context():
            print("\n📋 STEP 1: Prepare Test User")
            print("─" * 70)
            
            # Get or create test user
            user = User.query.filter_by(email_address=app.config['MAIL_DEFAULT_SENDER']).first()
            
            if not user:
                user = User(
                    full_name="Test User",
                    email_address=app.config['MAIL_DEFAULT_SENDER'],
                    user_province="Metro Manila",
                    user_city="Manila"
                )
                database.session.add(user)
                database.session.flush()
                
                settings = NotificationSettings(
                    user_id=user.id,
                    magnitude_threshold=3.5,
                    monitor_location_type='near_me',
                    add_safety_tips=True,
                    proximity_range_km=100.0
                )
                database.session.add(settings)
                database.session.commit()
                print("✅ Test user created")
            else:
                settings = NotificationSettings.query.filter_by(user_id=user.id).first()
                print("✅ Using existing user")
            
            print(f"   Name: {user.full_name}")
            print(f"   Email: {user.email_address}")
            print(f"   Location: {user.user_city}, {user.user_province}")
            print(f"   Magnitude threshold: {settings.magnitude_threshold}")
            
            print("\n📋 STEP 2: Simulate Earthquake Data")
            print("─" * 70)
            
            earthquake_data = {
                'date_time': '2024-11-08 16:45:00 PST',
                'latitude': '14.6760',
                'longitude': '121.0437',
                'depth': '12 km',
                'magnitude': '4.8',
                'location': '8 km E of Quezon City, Metro Manila',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/2024/integration-test'
            }
            
            print(f"   Time: {earthquake_data['date_time']}")
            print(f"   Location: {earthquake_data['location']}")
            print(f"   Magnitude: {earthquake_data['magnitude']}")
            print(f"   Depth: {earthquake_data['depth']}")
            print(f"   Coordinates: {earthquake_data['latitude']}, {earthquake_data['longitude']}")
            
            magnitude = LocationAnalyzer.parse_magnitude(earthquake_data['magnitude'])
            
            print("\n📋 STEP 3: Check User Criteria")
            print("─" * 70)
            
            print(f"   User threshold: {settings.magnitude_threshold}")
            print(f"   Earthquake magnitude: {magnitude}")
            
            if magnitude >= settings.magnitude_threshold:
                print(f"   ✅ Magnitude criteria met")
            else:
                print(f"   ❌ Magnitude below threshold")
                return False
            
            # Check location
            lat, lon = LocationAnalyzer.parse_coordinates(
                earthquake_data['latitude'],
                earthquake_data['longitude']
            )
            
            impact_radius = LocationAnalyzer.calculate_affected_radius(magnitude)
            print(f"   Impact radius: {impact_radius:.1f} km")
            
            is_affected = LocationAnalyzer.is_location_affected(
                user.user_province,
                user.user_city,
                (lat, lon),
                min(impact_radius, settings.proximity_range_km)
            )
            
            if is_affected:
                print(f"   ✅ Location criteria met")
            else:
                print(f"   ⚠️  Location outside range (test will continue anyway)")
            
            print("\n📋 STEP 4: Generate AI Summary")
            print("─" * 70)
            
            print("🤖 Calling Gemini AI...")
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            summary = summarizer.create_summary(earthquake_data, settings.add_safety_tips)
            
            print("✅ Summary generated:")
            print("─" * 70)
            print(summary)
            print("─" * 70)
            
            print("\n📋 STEP 5: Compose Email")
            print("─" * 70)
            
            subject = f"🚨 Earthquake Alert - Magnitude {earthquake_data['magnitude']}"
            
            body = f"""🚨 EARTHQUAKE NOTIFICATION 🚨

Dear {user.full_name},

{summary}

---
EARTHQUAKE DETAILS:
• Time: {earthquake_data['date_time']}
• Location: {earthquake_data['location']}
• Magnitude: {earthquake_data['magnitude']}
• Depth: {earthquake_data['depth']}
• Coordinates: {earthquake_data['latitude']}, {earthquake_data['longitude']}

Your monitored location: {user.user_city}, {user.user_province}
Full bulletin: {earthquake_data.get('detail_link', 'N/A')}

---
This is a TEST notification from the Index0 Earthquake Monitoring System.
You can update your preferences in your dashboard.

Stay safe!"""

            print(f"   To: {user.email_address}")
            print(f"   Subject: {subject}")
            print(f"   Body length: {len(body)} characters")
            
            print("\n📋 STEP 6: Send Email")
            print("─" * 70)
            
            msg = Message(
                subject=subject,
                recipients=[user.email_address],
                body=body
            )
            
            print("📨 Sending email via Flask-Mail...")
            email_service.send(msg)
            
            print("✅ Email sent successfully!")
            
            print("\n" + "=" * 70)
            print("🎉 INTEGRATION TEST COMPLETED SUCCESSFULLY")
            print("=" * 70)
            print("\n📬 CHECK YOUR EMAIL INBOX!")
            print(f"   Recipient: {user.email_address}")
            print(f"   Subject: {subject}")
            print("\n✅ The complete flow is working:")
            print("   1. ✓ User data retrieved from database")
            print("   2. ✓ Earthquake data processed")
            print("   3. ✓ User criteria checked")
            print("   4. ✓ AI summary generated (Gemini)")
            print("   5. ✓ Email composed with personalization")
            print("   6. ✓ Email sent successfully")
            print("=" * 70)
            
            return True
            
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_celery_task_simulation():
    """Simulate what the Celery task does"""
    print("\n" + "=" * 70)
    print("🔄 CELERY TASK SIMULATION")
    print("=" * 70)
    
    try:
        from app import build_application, database
        from app.models import User, NotificationSettings
        from app.location_service import LocationAnalyzer
        
        app = build_application()
        
        with app.app_context():
            print("\n📊 Simulating Celery task logic...")
            
            # Simulate fetching earthquake data
            print("\n1. Fetch latest earthquake from PHIVOLCS")
            print("   (Simulated - using test data)")
            
            bulletin_data = {
                'date_time': '2024-11-08 17:00:00 PST',
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '10 km',
                'magnitude': '4.2',
                'location': '5 km NW of Manila, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test'
            }
            
            magnitude = LocationAnalyzer.parse_magnitude(bulletin_data['magnitude'])
            print(f"   ✓ Magnitude: {magnitude}")
            
            # Check against all users
            print("\n2. Query all active users")
            all_users = User.query.filter_by(is_active=True).all()
            print(f"   ✓ Found {len(all_users)} active user(s)")
            
            affected_count = 0
            
            print("\n3. Check each user's criteria")
            for user in all_users:
                settings = NotificationSettings.query.filter_by(user_id=user.id).first()
                
                if not settings:
                    print(f"   ⊗ {user.full_name}: No settings configured")
                    continue
                
                print(f"\n   Checking: {user.full_name}")
                print(f"   • Magnitude: {magnitude} vs threshold {settings.magnitude_threshold}")
                
                if magnitude >= settings.magnitude_threshold:
                    print(f"     ✓ Magnitude criteria met")
                    
                    # Would send email here
                    print(f"     ✓ Would send email to: {user.email_address}")
                    affected_count += 1
                else:
                    print(f"     ✗ Below magnitude threshold")
            
            print(f"\n4. Summary")
            print(f"   Total users checked: {len(all_users)}")
            print(f"   Notifications that would be sent: {affected_count}")
            
            print("\n✅ Celery task simulation completed")
            return True
            
    except Exception as e:
        print(f"\n❌ Celery simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run integration tests"""
    print("\n" + "=" * 70)
    print("🚀 AI + EMAIL INTEGRATION TEST")
    print("=" * 70)
    
    print("\n⚠️  This test will:")
    print("   • Generate AI summaries using Gemini")
    print("   • Send test emails to your configured address")
    print("   • Simulate the complete notification workflow")
    
    input("\nPress ENTER to continue or Ctrl+C to cancel...")
    
    tests = [
        ("Complete Notification Flow", test_complete_notification_flow),
        ("Celery Task Simulation", test_celery_task_simulation),
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
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 70)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 70)
    if passed == total:
        print(f"🎉 ALL INTEGRATION TESTS PASSED ({passed}/{total})")
        print("\n✅ System is fully operational!")
        print("\n📬 You should have received an email with:")
        print("   • AI-generated earthquake summary")
        print("   • Personalized user information")
        print("   • Complete earthquake details")
        print("\n🎯 The system is ready to monitor earthquakes!")
    else:
        print(f"⚠️ SOME TESTS FAILED ({passed}/{total} passed)")
        print("\n❌ Please review the failures above")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
        sys.exit(1)
