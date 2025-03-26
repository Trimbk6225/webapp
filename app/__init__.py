from flask import Flask
from app.utils.db import db
from app.routes.health_check import health_check_blueprint
from flask_migrate import Migrate
from app.config import Config, TestConfig
from sqlalchemy import create_engine, text
from app.routes.files import files_blueprint
from app.utils.logger import webapp_logger

migrate = Migrate()

def create_test_database():
    """Create a new test database in MySQL"""
    test_db_url = f"mysql+pymysql://{Config().SQLALCHEMY_DATABASE_URI.split('/')[-2]}/"
    engine = create_engine(test_db_url)
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS test_healthcheckdb"))
        conn.execute(text("CREATE DATABASE test_healthcheckdb"))

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "testing":
        create_test_database()
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(files_blueprint)

    with app.app_context():
        db.create_all()

    webapp_logger.info("Application started")
    return app