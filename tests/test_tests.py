import unittest
from app import create_app
from app.utils.db import db
from app.models.health_check import HealthCheck
from datetime import datetime

class HealthCheckTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test app and database"""
        self.app = create_app("testing")  # Ensure 'testing' config exists
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check_creation(self):
        """Test if a HealthCheck record can be created"""
        with self.app.app_context():
            health_entry = HealthCheck(datetime=datetime.utcnow())
            db.session.add(health_entry)
            db.session.commit()
            
            result = HealthCheck.query.first()
            self.assertIsNotNone(result)
            self.assertIsInstance(result.datetime, datetime)

if __name__ == "__main__":
    unittest.main()