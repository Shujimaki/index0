# 🌋 Index0 - Earthquake Monitoring & Alert System

Automated earthquake monitoring system that sends personalized email alerts based on user preferences using AI-powered summaries.

## ✨ Features

- **User Authentication**: Login and registration system
- **Personalized Alerts**: Set magnitude thresholds and location preferences
- **AI Summaries**: Gemini AI generates easy-to-understand earthquake summaries
- **Email Notifications**: Automatic emails when conditions are met
- **Location-Based**: Monitor earthquakes near your location or custom locations
- **Safety Tips**: Optional safety recommendations for significant earthquakes
- **Real-time Monitoring**: Checks PHIVOLCS every 5 minutes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis (for Celery task queue)
- Gmail account (for sending emails)
- Gemini AI API key

### 1. Install Redis

```bash
# macOS
brew install redis
brew services start redis

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

### 2. Configure Environment Variables

Update `.env` file with your credentials:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///data.db
PORT=5001

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Redis & Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Note for Gmail:**
- Enable 2-Factor Authentication
- Generate an App Password: https://myaccount.google.com/apppasswords
- Use the App Password (not your regular password)

### 3. Run Setup Script

```bash
./setup.sh
```

This will:
- Create virtual environment
- Install dependencies
- Initialize database
- Run migrations

### 4. Start the Application

Open **3 terminal windows** and run:

**Terminal 1 - Flask Web Server:**
```bash
python run.py
```

**Terminal 2 - Celery Worker:**
```bash
celery -A celery_worker.task_queue worker --loglevel=info
```

**Terminal 3 - Celery Beat Scheduler:**
```bash
celery -A celery_worker.task_queue beat --loglevel=info
```

### 5. Access the Application

Open your browser and go to:
```
http://localhost:5001
```

## 📖 User Guide

### Registration

1. Click "Sign Up" on the login page
2. Enter your name and email
3. Select your Region, Province, and City
4. Click "Register"

### Login

1. Enter your email as username
2. (Password field is for future implementation)
3. Click "LOGIN"

### Dashboard Settings

**Minimum Earthquake Magnitude:**
- Use slider to set threshold (1.0 - 9.0)
- Only earthquakes meeting or exceeding this magnitude will trigger alerts

**Location Preference:**
- **Near Me**: Monitor earthquakes near your registered location
- **Custom Location**: Monitor a different region/province/city

**Alert Radius:**
- Set the distance (in km) within which earthquakes will trigger alerts
- Default: 100km

**Safety Tips:**
- Check to include AI-generated safety recommendations
- Only included for earthquakes with magnitude ≥ 4.0

### Saving Preferences

Click the **"Save"** button to update your notification settings.

## 🔧 System Architecture

```
┌─────────────────┐
│  PHIVOLCS API   │ ← Scrapes earthquake data every 5 minutes
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Celery Beat    │ ← Scheduler triggers tasks
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Celery Worker  │ ← Processes earthquake data
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Flask App      │ ← Checks user preferences
│  + Database     │
└────────┬────────┘
         │
         ├→ Gemini AI (Generate summaries)
         │
         └→ Flask-Mail (Send emails)
```

## 📂 Project Structure

```
index0/
├── app/
│   ├── __init__.py          # App initialization
│   ├── routes.py            # Web routes & API endpoints
│   ├── models.py            # Database models
│   ├── tasks.py             # Celery tasks
│   ├── api.py               # PHIVOLCS scraper
│   ├── gemini_service.py    # AI summary generator
│   ├── location_service.py  # Location analysis
│   ├── ph_locations.py      # Philippine locations data
│   ├── cities.py            # Region/Province/City data
│   ├── celery_config.py     # Celery schedule config
│   ├── templates/           # HTML templates
│   │   ├── auth_page.html
│   │   └── dashboard.html
│   └── static/              # CSS, images, JS
├── migrations/              # Database migrations
├── config.py               # Configuration
├── run.py                  # Flask app entry point
├── celery_worker.py        # Celery entry point
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script
└── .env                   # Environment variables
```

## 🧪 Testing

### Test Email Sending

```python
from app import build_application, email_service
from flask_mail import Message

app = build_application()
with app.app_context():
    msg = Message(
        subject="Test Email",
        recipients=["your-email@gmail.com"],
        body="This is a test email from Index0."
    )
    email_service.send(msg)
    print("✅ Email sent!")
```

### Test Celery Task Manually

```python
from celery_worker import flask_app
from app.tasks import check_and_process_earthquakes

with flask_app.app_context():
    result = check_and_process_earthquakes()
    print(result)
```

### Test Gemini AI

```python
from app import build_application
from app.gemini_service import GeminiSummarizer

app = build_application()
with app.app_context():
    summarizer = GeminiSummarizer(app.config['GEMINI_API_KEY'])
    
    test_data = {
        'date_time': '2024-11-08 10:30:00 PST',
        'latitude': '14.5995',
        'longitude': '120.9842',
        'depth': '10 km',
        'magnitude': '4.5',
        'location': 'Manila, Philippines',
        'detail_link': 'https://example.com/test'
    }
    
    summary = summarizer.create_summary(test_data, include_safety_tips=True)
    print(summary)
```

## ⚠️ Important Security Notes

### Email Credentials

The `.env` file in this repository contains a **real Gemini API key**. This is **NOT RECOMMENDED** for production use.

**Best Practices:**
1. Never commit `.env` files to version control
2. Add `.env` to `.gitignore`
3. Use environment variables in production
4. Rotate API keys regularly
5. Use secret management services (AWS Secrets Manager, Azure Key Vault, etc.)

### Production Deployment

Before deploying to production:

1. **Update SECRET_KEY**: Generate a secure random key
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Use PostgreSQL**: Replace SQLite with PostgreSQL
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

3. **Add Password Authentication**: Implement proper password hashing
   - Use `werkzeug.security` or `bcrypt`
   - Add password field to User model

4. **Enable HTTPS**: Use SSL certificates for secure communication

5. **Rate Limiting**: Add rate limiting to prevent abuse

6. **Error Monitoring**: Integrate Sentry or similar service

7. **Logging**: Configure proper logging with rotation

## 🛠️ Troubleshooting

### Redis Connection Error

```
Error: Error connecting to Redis
```

**Solution:**
```bash
# Start Redis
brew services start redis

# Or manually
redis-server
```

### Celery Not Processing Tasks

```bash
# Check if Celery worker is running
celery -A celery_worker.task_queue inspect active

# Purge all pending tasks
celery -A celery_worker.task_queue purge
```

### Email Not Sending

1. Check Gmail App Password is correct
2. Verify 2FA is enabled on Gmail account
3. Check MAIL_USERNAME and MAIL_DEFAULT_SENDER are the same
4. Look for error messages in Celery worker logs

### Database Migration Issues

```bash
# Delete migrations and start fresh
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Gemini AI Errors

1. Verify API key is correct
2. Check API quota/limits
3. Review error messages in Celery worker logs
4. Fallback summary will be used if AI fails

## 📝 Development

### Adding New Features

1. **New Route:**
   - Add route in `app/routes.py`
   - Create template in `app/templates/`

2. **New Database Model:**
   - Add model in `app/models.py`
   - Run migrations:
     ```bash
     flask db migrate -m "Description"
     flask db upgrade
     ```

3. **New Celery Task:**
   - Add task in `app/tasks.py`
   - Update schedule in `app/celery_config.py`

### Code Style

- Follow PEP 8
- Use type hints where applicable
- Add docstrings to functions
- Keep functions small and focused

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
1. Check this README first
2. Review error logs
3. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Password authentication
- [ ] SMS notifications
- [ ] Mobile app
- [ ] Historical earthquake data
- [ ] Data visualization dashboard
- [ ] Multi-language support
- [ ] Webhook notifications
- [ ] Admin panel
- [ ] User preference export/import

---

**Built with:**
- Flask
- Celery
- Redis
- Gemini AI
- BeautifulSoup4
- SQLAlchemy
- Flask-Mail

**Data Source:** PHIVOLCS (Philippine Institute of Volcanology and Seismology)
