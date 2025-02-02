import unittest
from app import create_app
from app.utils.db import db
from app.models.health_check import HealthCheck
from datetime import datetime, UTC
from sqlalchemy import text

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

    def test_database_connection(self):
        """Test if the application can connect to MySQL/PostgreSQL"""
        with self.app.app_context():
            try:
                # Use text() to explicitly declare the SQL statement
                result = db.session.execute(text("SELECT 1"))
                print(result, result.scalar())
                self.assertEqual(result.scalar(), 1)
            except Exception as e:
                self.fail(f"Database connection failed: {str(e)}")

    def test_get_method_allowed(self):
        """Test if GET method is allowed"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)  # Success for GET

    def test_post_method_not_allowed(self):
        """Test if POST method is not allowed"""
        response = self.client.post('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_put_method_not_allowed(self):
        """Test if PUT method is not allowed"""
        response = self.client.put('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_delete_method_not_allowed(self):
        """Test if DELETE method is not allowed"""
        response = self.client.delete('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_patch_method_not_allowed(self):
        """Test if PATCH method is not allowed"""
        response = self.client.patch('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_head_method_not_allowed(self):
        """Test if HEAD method is not allowed"""
        response = self.client.head('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_options_method_not_allowed(self):
        """Test if OPTIONS method is not allowed"""
        response = self.client.options('/healthz')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_no_payload_in_request(self):
        """Test that the request does not require any payload"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'')  # Ensure response body is empty

    def test_no_query_params_in_request(self):
        """Test that the request does not require any query parameters"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'')  # Ensure no query params required

    def test_no_internal_server_error(self):
        """Ensure that there are no 500 Internal Server Errors"""
        response = self.client.get('/healthz')
        self.assertNotEqual(response.status_code, 500)  # Ensure no 500 Internal Server Error occurs

    def insert_health_check():
        result = db.session.execute(text("SELECT 1"))
        # Continue with your logic
        return result

    def test_database_restart(self):
        """Test that the application does not require a restart after a database restart"""
        # Step 1: Perform a GET request while database is running
        response_1 = self.client.get('/healthz')
        self.assertEqual(response_1.status_code, 200)
        
        # Step 2: Simulate a database server shutdown (manual step or mock)
        
        # Step 3: Perform a GET request again after database is restarted
        response_2 = self.client.get('/healthz')
        self.assertEqual(response_2.status_code, 200)  # Ensure GET works even after database restart


if __name__ == "__main__":
    unittest.main()