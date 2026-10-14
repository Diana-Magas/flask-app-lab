import unittest
from app import app 

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /users/hi/<name>."""
        response = self.client.get("/users/hi/Diana?age=20")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DIANA", response.data)
        self.assertIn(b"20", response.data)

    def test_admin_page(self):
        """Тест маршруту /users/admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DIANA", response.data)
        self.assertIn(b"20", response.data)


if __name__ == "__main__":
    unittest.main()