# 🌋 YANIG - Earthquake Monitoring & Notification System

**Your Automated Notification for Intense Groundshaking**

An intelligent earthquake monitoring system that automatically sends personalized email notifications to users when earthquakes from PHIVOLCS match their preferences. Powered by AI-generated summaries using Google Gemini.

---

## 🎯 Features

- **🔔 Automatic Monitoring**: Checks PHIVOLCS earthquake bulletins every 5 minutes
- **🤖 AI-Powered Summaries**: Generates easy-to-understand earthquake summaries using Google Gemini 2.0
- **📧 Email Notifications**: Sends personalized alerts to users based on their preferences
- **⚙️ Customizable Settings**: Users can set magnitude thresholds and location preferences
- **🧪 Test Functionality**: Users can simulate earthquakes to test their notification settings
- **🛡️ Duplicate Prevention**: Ensures users receive each earthquake notification only once
- **📊 Safety Tips**: Optionally includes safety recommendations for significant earthquakes (≥ 4.0)

---

## 🏗️ Technology Stack

### Backend
- **Python 3.14**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Mail** - Email sending
- **Celery** - Background task processing
- **Redis** - Message broker and caching

### AI & Data
- **Google Gemini 2.0 Flash** - AI summary generation
- **BeautifulSoup4** - Web scraping PHIVOLCS bulletins
- **geopy** - Location distance calculations

### Frontend
- **HTML/CSS/JavaScript**
- **Tailwind CSS** - Styling
- **Jinja2** - Template engine

### Database
- **SQLite** (Development)
- PostgreSQL recommended for production

---

## 📋 Prerequisites

- Python 3.14 or higher
- Redis server
- Gmail account with 2FA enabled (for email notifications)
- Google Gemini API key

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Shujimaki/index0.git
cd index0
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Redis
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///data.db

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Not your regular password!
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
```

**Important:** 
- For `MAIL_PASSWORD`, use a Gmail App Password, not your regular password
- Enable 2FA on your Gmail account first
- Generate App Password at: https://myaccount.google.com/apppasswords

### 6. Initialize Database
```bash
flask db upgrade
```

Or if migrations folder doesn't exist:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Add Existing Users Password Field (if upgrading)
```bash
python migrate_add_password.py
```

---

## 🎮 Running the Application

You need **3 terminal windows** to run the complete system:

### Terminal 1: Flask Web Server
```bash
python run.py
```
Access at: http://localhost:5001

### Terminal 2: Celery Worker (Task Processor)
```bash
celery -A celery_worker.task_queue worker --loglevel=info
```

### Terminal 3: Celery Beat (Scheduler)
```bash
celery -A celery_worker.task_queue beat --loglevel=info
```

---

## 📱 Usage

### 1. Register an Account
- Visit http://localhost:5001
- Click "Sign Up"
- Enter your details:
  - Full name (used for login)
  - Email address
  - Password (minimum 6 characters)
  - Location (Region → Province → City)

### 2. Configure Preferences
In your dashboard, set:
- **Minimum Magnitude**: 1.0 - 9.0 (in 0.5 increments)
- **Location Preference**:
  - **Near Me**: Monitor earthquakes in your registered location
  - **Custom**: Select a different location to monitor
- **Safety Tips**: Include safety recommendations for magnitude ≥ 4.0

### 3. Test Your Settings
- Scroll to "🧪 Test Email Notification" section
- Set test magnitude and location
- Click "🚀 Run Test"
- Check if email would be sent based on your settings
- If criteria match, you'll receive an actual test email

### 4. Automatic Monitoring
Once running, the system will:
- Check PHIVOLCS every 5 minutes
- Process new earthquake bulletins
- Generate AI summaries
- Send emails to matching users automatically

---

## 🧪 Testing

### Run All Tests
```bash
# System checks
python test_system.py

# AI functionality
python test_ai_gemini.py

# Email system
python test_email_system.py

# Integration tests
python test_integration.py

# Quick manual test
python test_quick.py
```

### Check Monitoring Status
```bash
python check_monitoring_status.py
```

---

## 📊 Database Schema

### User
- `id`: Primary key
- `full_name`: User's full name (used as username)
- `email_address`: Unique email
- `password_hash`: Hashed password
- `user_province`: Registered province
- `user_city`: Registered city
- `is_active`: Account status

### NotificationSettings
- `user_id`: Foreign key to User
- `magnitude_threshold`: Minimum magnitude (default: 3.0)
- `monitor_location_type`: 'near_me' or 'custom'
- `alternate_province`: Custom province (if custom)
- `alternate_city`: Custom city (if custom)
- `add_safety_tips`: Include safety tips (default: True)
- `proximity_range_km`: Location radius (default: 100km)

### SeismicEvent
- `event_identifier`: Unique event ID
- `event_magnitude`: Earthquake magnitude
- `event_location`: Location description
- `latitude`, `longitude`: Coordinates
- `depth`: Depth in km
- `has_been_processed`: Prevents duplicate notifications

---

## 🔧 Configuration

### Celery Beat Schedule
Earthquake checks run every **5 minutes** (300 seconds). To modify:

```python
# In app/celery_config.py
beat_schedule = {
    'check-earthquakes-every-5-minutes': {
        'task': 'app.tasks.check_and_process_earthquakes',
        'schedule': 300.0,  # Change this value (in seconds)
    }
}
```

### Email Template
Email notifications include:
- AI-generated summary
- Earthquake details (time, location, magnitude, depth, coordinates)
- User's monitored location
- Link to official PHIVOLCS bulletin
- PHIVOLCS source attribution
- AI disclaimer
- Safety tips (if enabled and magnitude ≥ 4.0)

---

## 🐛 Troubleshooting

### Email Not Sending
1. Verify Gmail App Password (not regular password)
2. Ensure 2FA is enabled on Gmail
3. Check `.env` file configuration
4. Test with: `python test_email_system.py`

### AI Summaries Not Generating
1. Verify `GEMINI_API_KEY` in `.env`
2. Check API key validity at Google AI Studio
3. Test with: `python test_ai_gemini.py`

### Celery Not Running
1. Ensure Redis is running: `redis-cli ping`
2. Check Celery worker logs for errors
3. Restart worker and beat processes

### No Earthquakes Being Processed
1. Check PHIVOLCS website accessibility
2. Verify Celery Beat is running
3. Check if earthquakes meet minimum magnitude (≥ 3.0)
4. Review Celery worker logs

---

## 📁 Project Structure

```
index0/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── api.py                   # PHIVOLCS scraper
│   ├── celery_config.py         # Celery configuration
│   ├── cities.py                # Philippine geography data
│   ├── gemini_service.py        # AI summary generation
│   ├── location_service.py      # Location analysis
│   ├── models.py                # Database models
│   ├── ph_locations.py          # Location coordinates
│   ├── routes.py                # Web routes
│   ├── tasks.py                 # Celery background tasks
│   ├── static/                  # CSS, images
│   └── templates/               # HTML templates
├── migrations/                  # Database migrations
├── tests/                       # Test files
├── .env                        # Environment variables (create this)
├── config.py                   # App configuration
├── celery_worker.py            # Celery worker entry point
├── requirements.txt            # Python dependencies
├── run.py                      # Flask app entry point
└── README.md                   # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Developers:**
- index0

**Institution:** De La Salle University
**Organization:** Google Developer Groups on Campus - De La Salle University

---

## 🙏 Acknowledgments

- **PHIVOLCS** - Philippine Institute of Volcanology and Seismology for earthquake data
- **Google Gemini** - AI-powered summary generation
- **Flask Community** - Excellent web framework
- **Celery** - Powerful background task processing

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: brian_metrillo@dlsu.edu.ph

---

## ⚠️ Disclaimer

This system is designed to provide timely earthquake notifications based on official PHIVOLCS data. However:

- **Not a replacement** for official emergency alert systems
- AI summaries are generated for ease of understanding - always refer to official PHIVOLCS bulletins for authoritative information
- Email delivery depends on network connectivity and email service availability
- System checks PHIVOLCS every 5 minutes - there may be a delay

**Always follow official emergency protocols and guidance from local authorities during seismic events.**

---

## 🚀 Future Enhancements

- [ ] SMS notifications via Twilio
- [ ] Mobile app (iOS/Android)
- [ ] Real-time dashboard with WebSockets
- [ ] Historical earthquake data visualization
- [ ] Multi-language support
- [ ] Push notifications
- [ ] Earthquake prediction analytics
- [ ] Community reporting features

---

**Built with ❤️ for the safety of Filipinos**

*Last Updated: November 8, 2025*