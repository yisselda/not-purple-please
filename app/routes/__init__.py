from .themes import bp as themes_bp

def register_blueprints(app):
    app.register_blueprint(themes_bp, url_prefix="/v1/themes")
