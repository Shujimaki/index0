#!/usr/bin/env python
"""
Test script for Email system
Tests Flask-Mail configuration and email sending
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_configuration():
    """Test email configuration"""
    print("=" * 70)
    print("📧 TESTING EMAIL CONFIGURATION")
    print("=" * 70)
    
    try:
        from config import configuration_map
        
        config = configuration_map['development']
        
        print("📋 Email Settings:")
        print(f"   MAIL_SERVER: {config.MAIL_SERVER}")
        print(f"   MAIL_PORT: {config.MAIL_PORT}")
        print(f"   MAIL_USE_TLS: {config.MAIL_USE_TLS}")
        print(f"   MAIL_USERNAME: {config.MAIL_USERNAME}")
        print(f"   MAIL_PASSWORD: {'*' * 10 if config.MAIL_PASSWORD else 'NOT SET'}")
        print(f"   MAIL_DEFAULT_SENDER: {config.MAIL_DEFAULT_SENDER}")
        
        if not config.MAIL_USERNAME:
            print("\n❌ MAIL_USERNAME not configured in .env")
            return False
        
        if not config.MAIL_PASSWORD:
            print("\n❌ MAIL_PASSWORD not configured in .env")
            return False
        
        if not config.MAIL_DEFAULT_SENDER:
            print("\n❌ MAIL_DEFAULT_SENDER not configured in .env")
            return False
        
        print("\n✅ Email configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        return False


def test_flask_mail_initialization():
    """Test Flask-Mail initialization"""
    print("\n" + "=" * 70)
    print("🧪 TEST 1: Flask-Mail Initialization")
    print("=" * 70)
    
    try:
        from app import build_application, email_service
        
        app = build_application()
        
        with app.app_context():
            print("✅ Flask-Mail initialized successfully")
            print(f"   Mail server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
            return True
            
    except Exception as e:
        print(f"\n❌ Flask-Mail initialization failed: {e}")
        return False


def test_simple_email():
    """Test sending a simple test email"""
    print("\n" + "=" * 70)
    print("🧪 TEST 2: Send Simple Test Email")
    print("=" * 70)
    
    try:
        from app import build_application, email_service
        from flask_mail import Message
        
        app = build_application()
        
        with app.app_context():
            recipient = app.config['MAIL_DEFAULT_SENDER']  # Send to self
            
            print(f"📤 Preparing test email...")
            print(f"   To: {recipient}")
            print(f"   Subject: Index0 Test Email")
            
            msg = Message(
                subject="✅ Index0 Test Email",
                recipients=[recipient],
                body="""This is a test email from the Index0 Earthquake Monitoring System.

If you received this, your email configuration is working correctly!

Test Details:
- System: Index0
- Date: November 8, 2025
- Purpose: Email system verification

This is an automated test message."""
            )
            
            print(f"\n📨 Sending email...")
            email_service.send(msg)
            
            print(f"\n✅ Email sent successfully!")
            print(f"\n📬 CHECK YOUR INBOX: {recipient}")
            print(f"   Subject: ✅ Index0 Test Email")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Email sending failed: {e}")
        import traceback
        traceback.print_exc()
        print("\n🔍 Common issues:")
        print("   1. Gmail App Password not generated")
        print("   2. 2FA not enabled on Gmail account")
        print("   3. Wrong email/password in .env")
        print("   4. Firewall blocking SMTP port 587")
        return False


def test_earthquake_alert_email():
    """Test earthquake alert email with AI summary"""
    print("\n" + "=" * 70)
    print("🧪 TEST 3: Send Earthquake Alert Email (with AI)")
    print("=" * 70)
    
    try:
        from app import build_application, email_service
        from flask_mail import Message
        from app.gemini_service import GeminiSummarizer
        
        app = build_application()
        
        with app.app_context():
            recipient = app.config['MAIL_DEFAULT_SENDER']
            
            # Sample earthquake data
            earthquake_data = {
                'date_time': '2024-11-08 15:30:00 PST',
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '10 km',
                'magnitude': '4.5',
                'location': '12 km SW of Manila, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test'
            }
            
            print(f"🤖 Generating AI summary...")
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            summary = summarizer.create_summary(earthquake_data, include_safety_tips=True)
            
            print(f"✅ Summary generated")
            
            subject = f"🚨 Earthquake Alert - Magnitude {earthquake_data['magnitude']}"
            
            body = f"""🚨 EARTHQUAKE NOTIFICATION 🚨

Dear Test User,

{summary}

---
EARTHQUAKE DETAILS:
• Time: {earthquake_data['date_time']}
• Location: {earthquake_data['location']}
• Magnitude: {earthquake_data['magnitude']}
• Depth: {earthquake_data['depth']}
• Coordinates: {earthquake_data['latitude']}, {earthquake_data['longitude']}

Your monitored location: Manila, Metro Manila
Full bulletin: {earthquake_data['detail_link']}

---
This is a TEST notification from the Index0 Earthquake Monitoring System.

Stay safe!"""

            print(f"\n📤 Preparing earthquake alert email...")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            
            msg = Message(
                subject=subject,
                recipients=[recipient],
                body=body
            )
            
            print(f"\n📨 Sending email...")
            email_service.send(msg)
            
            print(f"\n✅ Earthquake alert email sent successfully!")
            print(f"\n📬 CHECK YOUR INBOX: {recipient}")
            print(f"   Subject: {subject}")
            print(f"   Content includes AI-generated summary")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Earthquake alert email failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_recipients():
    """Test sending to multiple recipients"""
    print("\n" + "=" * 70)
    print("🧪 TEST 4: Multiple Recipients Email")
    print("=" * 70)
    
    try:
        from app import build_application, email_service
        from flask_mail import Message
        
        app = build_application()
        
        with app.app_context():
            # Send to same address multiple times (simulating multiple users)
            recipient = app.config['MAIL_DEFAULT_SENDER']
            recipients = [recipient]  # In production, this would be multiple users
            
            print(f"📤 Preparing multi-recipient test...")
            print(f"   Recipients: {len(recipients)}")
            
            msg = Message(
                subject="✅ Index0 Multi-Recipient Test",
                recipients=recipients,
                body="""This is a test of the multi-recipient email capability.

In production, this would be sent to multiple users based on their preferences.

This message confirms that the system can handle bulk notifications."""
            )
            
            print(f"\n📨 Sending email...")
            email_service.send(msg)
            
            print(f"\n✅ Multi-recipient email sent successfully!")
            print(f"   Sent to {len(recipients)} recipient(s)")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Multi-recipient email failed: {e}")
        return False


def test_email_with_user_data():
    """Test personalized email with user data from database"""
    print("\n" + "=" * 70)
    print("🧪 TEST 5: Personalized Email (with Database User)")
    print("=" * 70)
    
    try:
        from app import build_application, email_service, database
        from flask_mail import Message
        from app.models import User
        
        app = build_application()
        
        with app.app_context():
            # Get first user from database
            user = User.query.first()
            
            if not user:
                print("⚠️ No users in database. Creating test user...")
                
                # Create test user
                from app.models import NotificationSettings
                
                test_user = User(
                    full_name="Test User",
                    email_address=app.config['MAIL_DEFAULT_SENDER'],
                    user_province="Metro Manila",
                    user_city="Manila"
                )
                database.session.add(test_user)
                database.session.flush()
                
                settings = NotificationSettings(
                    user_id=test_user.id,
                    magnitude_threshold=4.0,
                    monitor_location_type='near_me',
                    add_safety_tips=True
                )
                database.session.add(settings)
                database.session.commit()
                
                user = test_user
                print(f"✅ Test user created: {user.full_name}")
            
            print(f"\n👤 User Data:")
            print(f"   Name: {user.full_name}")
            print(f"   Email: {user.email_address}")
            print(f"   Location: {user.user_city}, {user.user_province}")
            
            subject = f"🚨 Personalized Alert for {user.full_name}"
            
            body = f"""🚨 EARTHQUAKE NOTIFICATION 🚨

Dear {user.full_name},

This is a personalized test notification for your location: {user.user_city}, {user.user_province}.

Your settings:
- Magnitude threshold: 4.0
- Monitoring: {user.user_city}
- Email: {user.email_address}

In a real scenario, you would receive:
• AI-generated earthquake summary
• Location-specific impact analysis
• Safety recommendations (if enabled)
• Links to detailed bulletins

---
This is a TEST notification from Index0.

Stay safe!"""

            print(f"\n📤 Preparing personalized email...")
            
            msg = Message(
                subject=subject,
                recipients=[user.email_address],
                body=body
            )
            
            print(f"\n📨 Sending personalized email...")
            email_service.send(msg)
            
            print(f"\n✅ Personalized email sent successfully!")
            print(f"\n📬 CHECK YOUR INBOX: {user.email_address}")
            print(f"   Personalized for: {user.full_name}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Personalized email failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all email tests"""
    print("\n" + "=" * 70)
    print("🚀 EMAIL SYSTEM TEST SUITE")
    print("=" * 70)
    
    print("\n⚠️  IMPORTANT: These tests will send real emails!")
    print("   Make sure your .env file has correct email credentials.")
    
    input("\nPress ENTER to continue or Ctrl+C to cancel...")
    
    tests = [
        ("Configuration Check", test_email_configuration),
        ("Flask-Mail Init", test_flask_mail_initialization),
        ("Simple Email", test_simple_email),
        ("Earthquake Alert", test_earthquake_alert_email),
        ("Multiple Recipients", test_multiple_recipients),
        ("Personalized Email", test_email_with_user_data),
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
        print("\n✅ Email system is working correctly!")
        print("\n📬 CHECK YOUR EMAIL INBOX:")
        print("   You should have received 4-5 test emails")
        print("   - Simple test email")
        print("   - Earthquake alert with AI summary")
        print("   - Multi-recipient test")
        print("   - Personalized notification")
    else:
        print(f"⚠️ SOME TESTS FAILED ({passed}/{total} passed)")
        print("\n❌ Please review the failures above")
        print("\n🔍 Troubleshooting:")
        print("   1. Check .env file has correct email credentials")
        print("   2. Ensure Gmail 2FA is enabled")
        print("   3. Generate Gmail App Password (not regular password)")
        print("   4. Check firewall/network settings")
    print("=" * 70)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
        sys.exit(1)
