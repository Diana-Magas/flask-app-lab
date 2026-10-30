import os  

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PRODUCTS_DB = os.path.join(BASE_DIR, "data", "products.json")
MAX_CONTENT_LENGTH = 2 * 1024 * 1024   # 2 МБ

SECRET_KEY = "dev-secret-key"