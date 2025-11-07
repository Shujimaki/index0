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