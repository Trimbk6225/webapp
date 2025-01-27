from flask import Flask
from app.utils.db import db
from app.routes.health_check import health_check_blueprint
from flask_migrate import Migrate

migrate = Migrate()  # Create a Migrate instance


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(health_check_blueprint)

    return app