from flask import Flask, Blueprint
from Backend.extensions import db, migrate, jwt
from Backend.config import Config


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)
    migrate.init_app(app)
    db.init_app(app)


        
    