import unittest

class FileAPITestCase(unittest.TestCase):
    
    def test_upload_file(self):
        response = self.client.post("/files", data={"file": (io.BytesIO(b"test content"), "test.txt")})
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
