import os
from datetime import datetime
from flask import current_app
from tinydb import TinyDB, Query


def _open():
    path = current_app.config["PRODUCTS_DB"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return TinyDB(path, ensure_ascii=False, indent=2)


def all_products():
    with _open() as db:
        return sorted(db.table("products").all(), key=lambda p: p["id"])


def get_product(product_id):
    with _open() as db:
        return db.table("products").get(Query().id == product_id)


def add_product(data):
    with _open() as db:
        table = db.table("products")
        new_id = max((p["id"] for p in table.all()), default=0) + 1
        table.insert({**data, "id": new_id,
                      "created_at": datetime.now().isoformat(timespec="seconds")})
        return new_id


def update_product(product_id, data):
    with _open() as db:      # id і created_at не передаємо, тому вони не змінюються
        db.table("products").update(data, Query().id == product_id)


def delete_product(product_id):
    with _open() as db:
        db.table("products").remove(Query().id == product_id)