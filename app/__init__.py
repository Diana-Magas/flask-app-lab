from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

from .config import config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    app.add_url_rule('/', endpoint='resume', view_func=views.resume)
    app.add_url_rule('/resume', endpoint='resume', view_func=views.resume)
    app.add_url_rule('/contacts', endpoint='contacts',
                     view_func=views.contacts, methods=['GET', 'POST'])
    app.add_url_rule('/homepage', endpoint='home', view_func=views.home)


    from .users import users_bp
    app.register_blueprint(users_bp)

    from .products import products_bp
    app.register_blueprint(products_bp)

    from .posts import post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app