import os

class Config:
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads
    # would go here: DB_URL, SECRET_KEY, ALLOWED_EXTENSIONS, etc.
