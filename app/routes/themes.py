from flask import Blueprint, current_app, jsonify, request

from app.services import InvalidThemeUpload, ThemeServiceError, get_theme_service

bp = Blueprint("themes", __name__)


@bp.post("/create-theme")
def create_theme():
    if "file" not in request.files:
        return jsonify({"error": "missing file field"}), 400

    upload = request.files["file"]

    shuffle_flag = request.form.get("shuffle", "true").strip().lower()
    shuffle = shuffle_flag not in {"false", "0", "no"}

    theme_service = get_theme_service()

    try:
        theme = theme_service.generate_theme(upload, shuffle=shuffle)
        return jsonify({"theme": theme}), 200
    except InvalidThemeUpload as exc:
        return jsonify({"error": str(exc)}), 400
    except ThemeServiceError:
        current_app.logger.exception("Failed to generate Slack theme from upload")
        return jsonify({"error": "failed to generate theme"}), 500
