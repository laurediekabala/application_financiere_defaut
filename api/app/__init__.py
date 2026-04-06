from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.prediction_routes import prediction_bp
    app.register_blueprint(prediction_bp, url_prefix="/api/v1")

    return app