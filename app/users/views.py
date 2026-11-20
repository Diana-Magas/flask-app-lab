from flask import (
    request, redirect, url_for, render_template,
    flash, make_response, current_app,
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from app import db
from . import users_bp
from .forms import RegistrationForm, LoginForm
from .models import User


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


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=User.hash_password(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("users.login"))
    return render_template("users/register.html", form=form, title="Register")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data)
        )
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You logged in successfully!", "success")
            return redirect(url_for("users.account"))
        flash("Error: Invalid email or password.", "danger")
    return render_template("users/login.html", form=form, title="Вхід")


@users_bp.route("/account")
@login_required
def account():
    return render_template("users/account.html", user=current_user,
                           title="Account")


@users_bp.route("/list")
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template("users/users_list.html", users=users, title="Users")


@users_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/profile")
@login_required
def profile():
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
        username=current_user.username,
        cookies=cookies,
        theme=theme,
    )


@users_bp.route("/profile/cookies/add", methods=["POST"])
@login_required
def add_cookie():
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
@login_required
def delete_cookie():
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
@login_required
def delete_all_cookies():
    session_cookie = current_app.config.get("SESSION_COOKIE_NAME", "session")
    response = make_response(redirect(url_for("users.profile")))

    for key in request.cookies:
        if key != session_cookie:
            response.delete_cookie(key)

    flash("Усі користувацькі кукі видалено!", "success")
    return response


@users_bp.route("/profile/theme/<string:theme>")
@login_required
def change_theme(theme):
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