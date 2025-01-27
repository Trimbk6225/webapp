from datetime import datetime
from app.models.health_check import HealthCheck
from app.utils.db import db

def insert_health_check():
    try:
        record = HealthCheck(datetime=datetime.utcnow())
        db.session.add(record)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False