from flask import Flask
from dotenv import dotenv_values

from . import views


def create_app():
    app = Flask(__name__)
    env = dotenv_values(".env")
    app.config["SECRET_KEY"] = env['SECRET_KEY']

    app.register_blueprint(views.main_bp)
    return app
