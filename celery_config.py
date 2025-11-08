from celery.schedules import crontab

beat_schedule = {
    'check-phivolcs-every-5-minutes': {
        'task': 'app.tasks.check_and_process_earthquakes',
        'schedule': 300.0,  # 5 minutes in seconds (300 seconds)
        'options': {
            'expires': 240.0,  # Task expires after 4 minutes if not executed
        }
    },
}

# Set to Philippine timezone
timezone = 'Asia/Manila'

# Enable UTC
enable_utc = True

# Task result expires after 1 hour
result_expires = 3600