"""
Celery worker entry point with Flask app context
Run with: celery -A celery_worker.task_queue worker --loglevel=info
"""
from app import build_application, task_queue
import os

# Create Flask app
flask_app = build_application(os.getenv('FLASK_ENV', 'development'))

# Push app context for Celery tasks
flask_app.app_context().push()

# Import tasks after app context is set
from app import tasks

# This makes the celery app accessible
# celery -A celery_worker.task_queue worker --loglevel=info
# celery -A celery_worker.task_queue beat --loglevel=info