
import unittest

from app import create_app


class ProductsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_product_list(self):
        """Перевірка маршруту /product."""
        response = self.client.get("/product")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail(self):
        """Перевірка деталей першого товару."""
        response = self.client.get("/product/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_detail_phone(self):
        """Перевірка деталей другого товару."""
        response = self.client.get("/product/2")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_not_found(self):
        """Перевірка неіснуючого товару."""
        response = self.client.get("/product/999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
