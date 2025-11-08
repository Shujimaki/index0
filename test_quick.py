#!/usr/bin/env python
"""
Quick manual test - Test AI and Email interactively
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("🚀 QUICK MANUAL TEST - AI & EMAIL")
    print("=" * 70)
    
    from app import build_application
    
    app = build_application()
    
    with app.app_context():
        # Test 1: AI Generation
        print("\n📋 TEST 1: AI Summary Generation")
        print("─" * 70)
        
        try:
            from app.gemini_service import GeminiSummarizer
            
            test_earthquake = {
                'date_time': '2024-11-08 20:00:00 PST',
                'latitude': '14.5995',
                'longitude': '120.9842',
                'depth': '10 km',
                'magnitude': '4.5',
                'location': 'Manila, Philippines',
                'detail_link': 'https://earthquake.phivolcs.dost.gov.ph/test'
            }
            
            print("🤖 Generating AI summary...")
            summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
            summary = summarizer.create_summary(test_earthquake, include_safety_tips=True)
            
            print("\n✅ AI Summary:")
            print("─" * 70)
            print(summary)
            print("─" * 70)
            print("\n✅ AI TEST PASSED")
            
        except Exception as e:
            print(f"\n❌ AI TEST FAILED: {e}")
            return 1
        
        # Test 2: Email Sending
        print("\n📋 TEST 2: Email Sending")
        print("─" * 70)
        
        response = input("\nDo you want to send a test email? (yes/no): ").lower()
        
        if response in ['yes', 'y']:
            try:
                from flask_mail import Message
                from app import email_service
                
                recipient = app.config['MAIL_DEFAULT_SENDER']
                
                subject = "🚨 Test Earthquake Alert from Index0"
                
                body = f"""🚨 EARTHQUAKE NOTIFICATION TEST

Dear User,

{summary}

---
EARTHQUAKE DETAILS:
• Time: {test_earthquake['date_time']}
• Location: {test_earthquake['location']}
• Magnitude: {test_earthquake['magnitude']}
• Depth: {test_earthquake['depth']}

This is a TEST notification from Index0.

Stay safe!"""

                msg = Message(
                    subject=subject,
                    recipients=[recipient],
                    body=body
                )
                
                print(f"\n📧 Sending email to: {recipient}")
                email_service.send(msg)
                
                print("\n✅ EMAIL TEST PASSED")
                print(f"\n📬 Check your inbox: {recipient}")
                
            except Exception as e:
                print(f"\n❌ EMAIL TEST FAILED: {e}")
                print("\n🔍 Common fixes:")
                print("   1. Check MAIL_PASSWORD in .env (should be App Password)")
                print("   2. Enable 2FA on Gmail")
                print("   3. Generate new App Password")
                return 1
        else:
            print("\n⊗ Email test skipped")
        
        print("\n" + "=" * 70)
        print("✅ MANUAL TEST COMPLETED")
        print("=" * 70)
        print("\n🎉 Both AI and Email systems are working!")
        
        return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled")
        sys.exit(1)
