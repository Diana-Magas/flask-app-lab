from flask import (
    request, redirect, url_for, render_template,
    flash, session, make_response, current_app,
)
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

    session_cookie = current_app.config.get("SESSION_COOKIE_NAME", "session")

    cookies = [
        {"key": key, "value": value}
        for key, value in request.cookies.items()
        if key != session_cookie
    ]

    theme = request.cookies.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["username"],
        cookies=cookies,
        theme=theme,
    )


@users_bp.route("/profile/cookies/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    seconds = request.form.get("seconds", "3600")
    session_cookie = current_app.config.get("SESSION_COOKIE_NAME", "session")

    if not key or key.lower() == session_cookie.lower():
        flash("Вкажіть коректний ключ кукі!", "error")
        return redirect(url_for("users.profile"))

    try:
        seconds = int(seconds)
        if seconds < 1:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути додатним числом секунд!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=seconds, samesite="Lax")

    flash(f"Кукі «{key}» успішно додано!", "success")
    return response


@users_bp.route("/profile/cookies/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    session_cookie = current_app.config.get("SESSION_COOKIE_NAME", "session")

    if key == session_cookie:
        flash("Не можна видалити кукі сесії цим способом!", "error")
        return redirect(url_for("users.profile"))

    if not key or key not in request.cookies:
        flash("Кукі з таким ключем не знайдено!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)

    flash(f"Кукі «{key}» успішно видалено!", "success")
    return response


@users_bp.route("/profile/cookies/delete-all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    session_cookie = current_app.config.get("SESSION_COOKIE_NAME", "session")
    response = make_response(redirect(url_for("users.profile")))

    for key in request.cookies:
        if key != session_cookie:
            response.delete_cookie(key)

    flash("Усі користувацькі кукі видалено!", "success")
    return response


@users_bp.route("/profile/theme/<string:theme>")
def change_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        "theme",
        theme,
        max_age=365 * 24 * 60 * 60,
        samesite="Lax",
    )

    flash("Кольорову схему змінено!", "success")
    return response