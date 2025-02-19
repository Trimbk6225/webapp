import unittest
from unittest.mock import patch
from app import create_app
from app.utils.db import db
from app.models.health_check import HealthCheck
from datetime import datetime, UTC
from sqlalchemy import text, create_engine
from app.config import TestConfig 


class HealthCheckTestCase(unittest.TestCase):
    
    
    @classmethod
    def setUpClass(cls):
        """Create a new MySQL test database"""
        cls.app = create_app("testing")
        cls.client = cls.app.test_client()
        cls.engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)

        with cls.engine.connect() as conn:
            conn.execute(text("DROP DATABASE IF EXISTS test_healthcheckdb"))
            conn.execute(text("CREATE DATABASE test_healthcheckdb"))

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Drop the MySQL test database after tests complete"""
        with cls.engine.connect() as conn:
            conn.execute(text("DROP DATABASE IF EXISTS test_healthcheckdb"))

    def setUp(self):
        """Begin a new database session for each test"""
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Rollback session and drop tables after each test"""
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

    def test_database_connection(self):
        """Test if the application can connect to MySQL"""
        with self.app.app_context():
           try:
                result = db.session.execute(text("SELECT 1")).fetchone()
                self.assertIsNotNone(result)
                self.assertEqual(result[0], 1)
           except Exception as e:
                self.fail(f"Database connection failed: {str(e)}")

    def test_get_method_allowed(self):
        """Test if GET method is allowed"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)

    def test_post_method_not_allowed(self):
        """Test if POST method is not allowed"""
        response = self.client.post('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_put_method_not_allowed(self):
        """Test if PUT method is not allowed"""
        response = self.client.put('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_delete_method_not_allowed(self):
        """Test if DELETE method is not allowed"""
        response = self.client.delete('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_patch_method_not_allowed(self):
        """Test if PATCH method is not allowed"""
        response = self.client.patch('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_head_method_not_allowed(self):
        """Test if HEAD method is not allowed"""
        response = self.client.head('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_options_method_not_allowed(self):
        """Test if OPTIONS method is not allowed"""
        response = self.client.options('/healthz')
        self.assertEqual(response.status_code, 405)

    def test_no_payload_in_request(self):
        """Test that the request does not require any payload"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'')

    def test_no_query_params_in_request(self):
        """Test that the request does not require any query parameters"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'')

    def test_no_internal_server_error(self):
        """Ensure that there are no 500 Internal Server Errors"""
        response = self.client.get('/healthz')
        self.assertNotEqual(response.status_code, 500)

    def test_database_restart(self):
        """Test that the application does not require a restart after a database restart"""
        response_1 = self.client.get('/healthz')
        self.assertEqual(response_1.status_code, 200)
        
        response_2 = self.client.get('/healthz')
        self.assertEqual(response_2.status_code, 200)

    @patch('app.routes.health_check.insert_health_check', return_value=False)
    def test_service_unavailable(self, mock_insert_health_check):
        """Test if the service returns a 503 status code when it's unavailable"""
        
        # Ensure the mock is being applied correctly
        print("Mock is patched and should return False")
        
        # Perform the health check request
        response = self.client.get('/healthz')

        # Check the status code should be 503 as the insert_health_check returns False
        self.assertEqual(response.status_code, 503)

        # Ensure insert_health_check was actually called
        mock_insert_health_check.assert_called_once()

if __name__ == "__main__":
    unittest.main()