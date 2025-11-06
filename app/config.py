import os

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads
    THEME_ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    # Future configuration (DB_URL, SECRET_KEY, etc.) can live here to keep the factory thin.
