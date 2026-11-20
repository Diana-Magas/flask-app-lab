from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .config import config


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Крок 13: розкоментуйте перед db.init_app(app)
    # app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    from . import views
    app.add_url_rule('/', endpoint='resume', view_func=views.resume)
    app.add_url_rule('/resume', endpoint='resume', view_func=views.resume)
    app.add_url_rule(
        '/contacts',
        endpoint='contacts',
        view_func=views.contacts,
        methods=['GET', 'POST']
    )
    app.add_url_rule('/homepage', endpoint='home', view_func=views.home)

    from .users import users_bp
    app.register_blueprint(users_bp)
    from .users.models import User

    from .products import products_bp
    app.register_blueprint(products_bp)
    from .products.models import Product

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix='/post')
    from .posts.models import Post, Tag

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app