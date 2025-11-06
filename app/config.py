import os


class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads
    THEME_ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    # Additional settings live here so the factory stays minimal.
