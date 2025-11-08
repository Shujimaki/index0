from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from celery import Celery
from config import configuration_map
import redis

database = SQLAlchemy()
migration_tool = Migrate()
email_service = Mail()
task_queue = Celery(__name__)
redis_client = None

def build_application(environment='development'):
    application = Flask(__name__)
    application.config.from_object(configuration_map[environment])

    database.init_app(application)
    email_service.init_app(application)

    global redis_client
    redis_client = redis.from_url(application.config['REDIS_URL'])

    # Configure Celery
    task_queue.conf.update(application.config)
    task_queue.conf.broker_url = application.config['CELERY_BROKER_URL']
    task_queue.conf.result_backend = application.config['CELERY_RESULT_BACKEND']
    
    # Load beat schedule
    from app.celery_config import beat_schedule, timezone
    task_queue.conf.beat_schedule = beat_schedule
    task_queue.conf.timezone = timezone

    from app import models
    
    migration_tool.init_app(application, database)

    with application.app_context():
        from app import routes
        application.register_blueprint(routes.bp)

    return application