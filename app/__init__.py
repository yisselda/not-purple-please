import os
from flask import Flask
from .config import Config
from .logging import configure_logging
from .routes import register_blueprints
from .services import init_app as init_services

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_logging(app)
    init_services(app)
    register_blueprints(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app
