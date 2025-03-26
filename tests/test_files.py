import pytest
from unittest.mock import patch, MagicMock
from app import create_app  # Assuming you have a factory function to create your Flask app
from app.models.file_metadata import FileMetadata
from datetime import datetime
import io

# @pytest.fixture
# def client():
#     """Fixture to set up the Flask test client with application context."""
#     app = create_app()
#     app.config['TESTING'] = True

#     # Push an application context for the tests
#     with app.app_context():
#         with app.test_client() as client:
#             yield client

# def test_upload_file_no_file(client):
#     """Test uploading without providing a file."""
#     response = client.post("/v1/file", content_type='multipart/form-data', data={})
    
#     assert response.status_code == 400
#     json_data = response.get_json()
#     assert json_data["error"] == "No file provided"



# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     return app.test_client()

# def test_upload_file_no_file(client):
#     response = client.post('/upload')  # No file sent
#     assert response is not None, "Response is None!"  # Debugging check
#     assert response.status_code == 400  # Expecting a 400 Bad Request
#     assert b"No file uploaded" in response.data  # Response should contain error message

# @patch("app.models.file_metadata.FileMetadata.query.filter_by")
# def test_get_file_not_found(mock_filter_by, client):
#     """Test retrieving a file that does not exist."""
#     mock_filter_by.return_value.first.return_value = None

#     response = client.get("/v1/file/nonexistent-id")

#     assert response.status_code == 404
#     json_data = response.get_json()
#     assert json_data["error"] == "File not found"

# @patch("app.models.file_metadata.FileMetadata.query.filter_by")
# def test_delete_file_not_found(mock_filter_by, client):
#     """Test deleting a file that does not exist."""
#     mock_filter_by.return_value.first.return_value = None

#     response = client.delete("/v1/file/nonexistent-id")

#     assert response.status_code == 404
#     json_data = response.get_json()
#     assert json_data["error"] == "File not found"
