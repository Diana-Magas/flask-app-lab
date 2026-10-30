import os
import shutil
import tempfile
import unittest

from app import app
from app.products import database as db


class ProductsCrudTestCase(unittest.TestCase):

    def setUp(self):
        """Тимчасова база і клієнт перед кожним тестом."""
        self.tmp_dir = tempfile.mkdtemp()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["PRODUCTS_DB"] = os.path.join(self.tmp_dir, "products.json")
        self.client = app.test_client()
        self.data = {
            "name": "Laptop",
            "content": "Потужний ноутбук",
            "price": "1200",
            "category": "electronics",
            "quantity": "10",
        }

    def tearDown(self):
        """Видаляємо тимчасову базу після кожного тесту."""
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # тести  TinyDB (database.py) -
    def test_db_add_and_get(self):
        """Create/Read: add_product ставить id і created_at."""
        with app.app_context():
            pid = db.add_product({"name": "Phone", "price": 800.0})
            product = db.get_product(pid)
        self.assertEqual(pid, 1)
        self.assertEqual(product["name"], "Phone")
        self.assertIn("created_at", product)

    def test_db_id_increment(self):
        """id збільшуються автоматично."""
        with app.app_context():
            first = db.add_product({"name": "A"})
            second = db.add_product({"name": "B"})
        self.assertEqual((first, second), (1, 2))

    def test_db_update_keeps_id_and_created_at(self):
        """Update: id і created_at не змінюються."""
        with app.app_context():
            pid = db.add_product({"name": "Old", "price": 1.0})
            created = db.get_product(pid)["created_at"]
            db.update_product(pid, {"name": "New", "price": 2.0})
            product = db.get_product(pid)
        self.assertEqual(product["name"], "New")
        self.assertEqual(product["id"], pid)
        self.assertEqual(product["created_at"], created)

    def test_db_delete(self):
        """Delete: товар зникає з бази."""
        with app.app_context():
            pid = db.add_product({"name": "Temp"})
            db.delete_product(pid)
            self.assertIsNone(db.get_product(pid))

    # тести маршрутів 
    def test_product_list_empty(self):
        """Read: порожній список відкривається."""
        response = self.client.get("/product")
        self.assertEqual(response.status_code, 200)

    def test_product_add(self):
        """Create: товар додається і видно у списку."""
        response = self.client.post("/product/add", data=self.data,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

    def test_product_add_invalid(self):
        """Create: невалідна назва, товар не додається."""
        self.data["name"] = "ab"
        self.client.post("/product/add", data=self.data)
        response = self.client.get("/product/1")
        self.assertEqual(response.status_code, 404)

    def test_product_detail(self):
        """Read: сторінка товару."""
        self.client.post("/product/add", data=self.data)
        response = self.client.get("/product/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_not_found(self):
        """Read: неіснуючий товар дає 404."""
        response = self.client.get("/product/999")
        self.assertEqual(response.status_code, 404)

    def test_product_edit(self):
        """Update: дані змінюються."""
        self.client.post("/product/add", data=self.data)
        self.data["name"] = "Phone"
        self.data["price"] = "800"
        response = self.client.post("/product/1/edit", data=self.data,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_delete(self):
        """Delete: товар видаляється через POST."""
        self.client.post("/product/add", data=self.data)
        response = self.client.post("/product/1/delete",
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/product/1")
        self.assertEqual(response.status_code, 404)

    def test_product_delete_get_not_allowed(self):
        """Delete: через GET заборонено (405)."""
        self.client.post("/product/add", data=self.data)
        response = self.client.get("/product/1/delete")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()