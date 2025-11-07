from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import configuration_map

database = SQLAlchemy()
migration_tool = Migrate()

def build_application(environment='development'):
    application = Flask(__name__)
    application.config.from_object(configuration_map[environment])

    database.init_app(application)

    from app import models
    
    migration_tool.init_app(application, database)

    with application.app_context():
        from app import routes
        application.register_blueprint(routes.bp)

    return application