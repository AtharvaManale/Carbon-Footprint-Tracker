from flask import Flask
from Backend.extensions import db, migrate
from Backend.config import Config
from Backend.routes import auth


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    migrate.init_app(app)
    db.init_app(app)

    app.register_blueprint(auth.auth, url_prefix = '/auth')

    from Backend.models import models