import os
import uuid
from flask import (render_template, redirect, url_for, flash,abort, current_app)
from . import products_bp
from . import database as db
from .forms import ProductForm, DeleteForm


def save_image(file):
    ext = file.filename.rsplit(".", 1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"                  
    folder = current_app.config.get(
        "UPLOAD_FOLDER", os.path.join(products_bp.static_folder, "uploads"))
    os.makedirs(folder, exist_ok=True)
    file.save(os.path.join(folder, name))
    return f"uploads/{name}"                          


def form_to_data(form):
    return {"name": form.name.data,
            "content": form.content.data or "",
            "price": round(float(form.price.data), 2),   # Decimal -> float для JSON
            "category": form.category.data,
            "quantity": form.quantity.data}


@products_bp.route("/product")
def product_list():
    return render_template("products/products.html", title="Товари",
                           products=db.all_products())


@products_bp.route("/product/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        data = form_to_data(form)
        data["image"] = save_image(form.image.data) if form.image.data else ""
        db.add_product(data)
        flash("Товар успішно додано", "success")
        return redirect(url_for("products.product_list"))       # PRG
    if form.is_submitted():
        flash("Виправте помилки у формі", "danger")
    return render_template("products/product_form.html",
                           title="Додати товар", form=form, product=None)


@products_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = db.get_product(product_id)
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", title=product["name"],
                           product=product, delete_form=DeleteForm())


@products_bp.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = db.get_product(product_id)
    if product is None:
        abort(404)
    form = ProductForm(data=product)           
    if form.validate_on_submit():
        data = form_to_data(form)
        if form.image.data:                     
            data["image"] = save_image(form.image.data)
        db.update_product(product_id, data)   
        flash("Товар оновлено", "success")
        return redirect(url_for("products.product_detail", product_id=product_id))
    if form.is_submitted():
        flash("Виправте помилки у формі", "danger")
    return render_template("products/product_form.html",
                           title="Редагувати товар", form=form, product=product)


@products_bp.route("/product/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    if db.get_product(product_id) is None:
        abort(404)
    if DeleteForm().validate_on_submit():      
        db.delete_product(product_id)
        flash("Товар видалено", "success")
    else:
        flash("Недійсний запит", "danger")
    return redirect(url_for("products.product_list"))