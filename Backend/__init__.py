from flask import Flask
from Backend.extensions import db, migrate
from Backend.config import Config
from Backend.routes import auth, analytics, auditor, sales


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    migrate.init_app(app, db)
    db.init_app(app)

    app.register_blueprint(auth.auth, url_prefix = "/auth")
    app.register_blueprint(analytics.analytics, url_prefix = "/analytics")
    app.register_blueprint(auditor.auditor, url_prefix = "/auditor")
    app.register_blueprint(sales.sales, url_prefix = "/sales")

    from Backend.models import models

    return app