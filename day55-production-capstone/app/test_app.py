import unittest
from app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "running")

    def test_health(self):
        self.assertEqual(self.client.get("/health").status_code, 200)

    def test_readiness(self):
        self.assertEqual(self.client.get("/ready").status_code, 200)

    def test_metrics(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"http_requests_total", response.data)

    def test_not_found(self):
        self.assertEqual(self.client.get("/missing").status_code, 404)

if __name__ == "__main__":
    unittest.main()
