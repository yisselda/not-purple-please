import os
from flask import Flask
from .config import Config
from .logging import configure_logging
from .routes import register_blueprints

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_logging(app)
    register_blueprints(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

