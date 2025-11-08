from celery.schedules import crontab

beat_schedule = {
    'check-earthquakes-every-5-minutes': {
        'task': 'app.tasks.check_and_process_earthquakes',  # Fixed task name
        'schedule': 300.0,
        'options': {
            'expires': 240.0,
        }
    },
}

timezone = 'Asia/Manila'
enable_utc = True
result_expires = 3600