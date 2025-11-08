import os
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, '.env'))


class BaseConfiguration:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    DB_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(project_root, "data.db")}')
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # Email settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Task Queue
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Redis for caching
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


class DevConfiguration(BaseConfiguration):
    DEBUG = True
    TESTING = False


class ProdConfiguration(BaseConfiguration):
    DEBUG = False
    TESTING = False


configuration_map = {
    'development': DevConfiguration,
    'production': ProdConfiguration,
    'default': ProdConfiguration
}