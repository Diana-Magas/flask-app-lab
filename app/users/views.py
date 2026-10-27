from flask import request, redirect, url_for, render_template, flash, session
from . import users_bp

USERNAME = "diana"
PASSWORD = "12345"


@users_bp.route("/hi/<string:name>")   # /users/hi/diana?age=20
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("users/hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="Diana", age=20, _external=True)
    print(to_url)
    return redirect(to_url)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль!", "error")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви успішно вийшли із системи.", "success")
    return redirect(url_for("users.login"))


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["username"],
    )