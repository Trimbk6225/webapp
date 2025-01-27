from app.utils.db import db

class HealthCheck(db.Model):
    __tablename__ = "healthz"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    datetime = db.Column(db.DateTime, nullable=False)  # Non-nullable timestamp