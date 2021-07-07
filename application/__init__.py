from dotenv import dotenv_values
from flask import Flask

from . import auth
from . import views


def create_app():
    app = Flask(__name__)
    env = dotenv_values(".env")
    app.config["SECRET_KEY"] = env['SECRET_KEY']

    auth.login_manager.init_app(app)

    app.register_blueprint(views.main_bp)
    app.register_blueprint(auth.auth_bp)

    return app
