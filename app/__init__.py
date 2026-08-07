from flask import Flask
from app.routes.code_routes import code_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(code_bp)
    return app
