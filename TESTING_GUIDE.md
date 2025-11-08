# 🧪 Testing Guide

## Available Test Scripts

### 1. **System Check** (`test_system.py`)
Verifies all components are properly configured and can be imported.

```bash
python test_system.py
```

**Tests:**
- All imports work
- Flask app initializes
- Database connection
- Regions data loaded
- Routes registered
- Celery configured
- Redis connection

---

### 2. **AI Testing** (`test_ai_gemini.py`)
Tests Gemini AI integration and earthquake summary generation.

```bash
python test_ai_gemini.py
```

**Tests:**
- ✅ Gemini API connection
- ✅ Simple text generation
- ✅ Earthquake summary without safety tips
- ✅ Earthquake summary with safety tips (magnitude ≥ 4.0)
- ⚠️ Redis caching (may fail if cache generates different text)
- ✅ Fallback summary (when AI fails)

**Expected Results:**
- 5-6 tests should pass
- You'll see AI-generated earthquake summaries
- Safety tips included for magnitude ≥ 4.0

---

### 3. **Email Testing** (`test_email_system.py`)
Tests Flask-Mail configuration and email sending.

```bash
python test_email_system.py
```

⚠️ **WARNING: This will send real emails to your configured address!**

**Tests:**
- Email configuration check
- Flask-Mail initialization
- Simple test email
- Earthquake alert email with AI summary
- Multiple recipients email
- Personalized email with database user

**Expected Results:**
- You should receive 4-5 test emails in your inbox
- Each email tests a different aspect of the system

**Prerequisites:**
- Gmail account with 2FA enabled
- App Password generated
- Correct credentials in `.env` file

---

### 4. **Integration Testing** (`test_integration.py`)
Tests the complete notification workflow (AI + Email + Database).

```bash
python test_integration.py
```

⚠️ **WARNING: This will generate AI summaries and send emails!**

**Tests:**
- Complete notification flow
  1. Get/create test user from database
  2. Simulate earthquake data
  3. Check user criteria (magnitude & location)
  4. Generate AI summary with Gemini
  5. Compose personalized email
  6. Send email via Flask-Mail
- Celery task simulation

**Expected Results:**
- Complete workflow executes successfully
- You receive an email with AI-generated summary
- All 2 tests pass

---

## Quick Test Commands

### Test Everything
```bash
# Run all tests in sequence
python test_system.py && \
python test_ai_gemini.py && \
python test_email_system.py && \
python test_integration.py
```

### Test Just AI
```bash
python test_ai_gemini.py
```

### Test Just Email
```bash
python test_email_system.py
```

### Test Complete Flow
```bash
python test_integration.py
```

---

## What Gets Tested

### ✅ AI System (Gemini)
- [x] API connection and authentication
- [x] Basic text generation
- [x] Earthquake summary generation
- [x] Safety tips inclusion (magnitude ≥ 4.0)
- [x] Fallback summaries when AI fails
- [x] Response formatting

### ✅ Email System (Flask-Mail)
- [x] SMTP configuration
- [x] Gmail connection
- [x] Simple email sending
- [x] Email with AI-generated content
- [x] Multiple recipients
- [x] Personalized emails
- [x] Database integration

### ✅ Integration
- [x] End-to-end notification flow
- [x] User criteria checking
- [x] Location analysis
- [x] Magnitude thresholds
- [x] AI + Email working together
- [x] Database operations

---

## Troubleshooting

### AI Tests Failing

**Problem:** `API key not valid`
```bash
# Check your .env file
cat .env | grep GEMINI_API_KEY
```
**Solution:** Ensure GEMINI_API_KEY is set correctly

**Problem:** `Rate limit exceeded`
**Solution:** Wait a few minutes and try again

---

### Email Tests Failing

**Problem:** `Authentication failed`
```bash
# Check email settings
cat .env | grep MAIL_
```

**Solutions:**
1. Enable 2FA on Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password (not regular password) in MAIL_PASSWORD
4. Ensure MAIL_USERNAME and MAIL_DEFAULT_SENDER are the same

**Problem:** `Connection timed out`
**Solution:** Check firewall settings, ensure port 587 is open

**Problem:** `SMTPAuthenticationError`
**Solution:** 
- Verify email and password are correct
- Make sure you're using an App Password, not your regular password
- Check if "Less secure app access" is disabled (it should be, use App Passwords)

---

### Redis/Caching Issues

**Problem:** Caching tests fail
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

**Solution:**
```bash
# Start Redis
brew services start redis

# Or manually
redis-server
```

---

## Test Results Interpretation

### All Green (✅)
- System is fully operational
- Ready for production use
- All features working correctly

### Partial Pass (⚠️)
- Core features work
- Some non-critical issues
- System usable but check warnings

### Failures (❌)
- Critical issues present
- Review error messages
- Fix configuration before proceeding

---

## Sample Test Output

### Successful AI Test
```
✅ PASS - Connection Test
✅ PASS - Simple Generation
✅ PASS - Summary Without Tips
✅ PASS - Summary With Tips
✅ PASS - Fallback Summary

🎉 ALL TESTS PASSED (5/6)
✅ Gemini AI is working correctly!
```

### Successful Email Test
```
✅ PASS - Configuration Check
✅ PASS - Flask-Mail Init
✅ PASS - Simple Email
✅ PASS - Earthquake Alert
✅ PASS - Multiple Recipients
✅ PASS - Personalized Email

🎉 ALL TESTS PASSED (6/6)
✅ Email system is working correctly!
📬 CHECK YOUR EMAIL INBOX
```

### Successful Integration Test
```
✅ PASS - Complete Notification Flow
✅ PASS - Celery Task Simulation

🎉 ALL INTEGRATION TESTS PASSED (2/2)
✅ System is fully operational!
📬 You should have received an email with AI summary
```

---

## Before Running Tests

### 1. Check .env Configuration
```bash
cat .env
```

Ensure these are set:
- `GEMINI_API_KEY` - Your Gemini AI API key
- `MAIL_USERNAME` - Your Gmail address
- `MAIL_PASSWORD` - Your Gmail App Password
- `MAIL_DEFAULT_SENDER` - Same as MAIL_USERNAME

### 2. Start Redis (for caching)
```bash
brew services start redis
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## After Running Tests

### Check Your Email
After running email tests, you should have received:
1. **Simple Test Email** - Basic functionality test
2. **Earthquake Alert** - With AI-generated summary
3. **Multi-Recipient Test** - Bulk sending capability
4. **Personalized Email** - Database integration test
5. **Integration Test Email** - Complete workflow test

### Review Logs
Check for any warnings or errors in the console output.

### Verify Database
```bash
sqlite3 data.db "SELECT * FROM users;"
```

Should show test users created during testing.

---

## Production Checklist

Before deploying to production, ensure:
- [ ] All tests pass (system, AI, email, integration)
- [ ] Environment variables properly set
- [ ] Email credentials secured
- [ ] API keys rotated
- [ ] Database migrations applied
- [ ] Redis running and accessible
- [ ] Celery worker and beat configured
- [ ] Monitoring and logging enabled

---

## Need Help?

1. **Review error messages** - They usually indicate the problem
2. **Check logs** - Look for detailed error information
3. **Verify configuration** - Double-check .env file
4. **Test incrementally** - Run system check first, then AI, then email
5. **Check prerequisites** - Ensure Redis, Python packages installed

---

**Testing ensures reliability! 🧪✅**
