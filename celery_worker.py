from app import build_application, task_queue
import os

# Create Flask app
flask_app = build_application(os.getenv('FLASK_ENV', 'development'))

# Push app context for Celery
flask_app.app_context().push()

# Import tasks after app context is set
from app import tasks