from __future__ import annotations

from flask import current_app

from app.domain.slack_theme import generate_slack_theme

from .theme_service import InvalidThemeUpload, ThemeService, ThemeServiceError

__all__ = [
    "InvalidThemeUpload",
    "ThemeService",
    "ThemeServiceError",
    "get_theme_service",
    "init_app",
]


def init_app(app) -> None:
    """Attach service singletons to the Flask app instance."""
    allowed = app.config.get("THEME_ALLOWED_EXTENSIONS")
    service = ThemeService(generator=generate_slack_theme, allowed_extensions=allowed)
    app.extensions["theme_service"] = service


def get_theme_service() -> ThemeService:
    service = current_app.extensions.get("theme_service")
    if service is None:
        raise RuntimeError("Theme service not initialized")
    return service
