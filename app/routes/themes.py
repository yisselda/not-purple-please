import os
import tempfile
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

from gen_slack_theme import generate_slack_theme

bp = Blueprint("themes", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def _is_allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@bp.post("/create-theme")
def create_theme():
    if "file" not in request.files:
        return jsonify({"error": "missing file field"}), 400

    upload = request.files["file"]

    if upload.filename == "":
        return jsonify({"error": "empty filename"}), 400

    if not _is_allowed_file(upload.filename):
        return jsonify({"error": "unsupported file type"}), 400

    shuffle_flag = request.form.get("shuffle", "true").strip().lower()
    shuffle = shuffle_flag not in {"false", "0", "no"}

    tmp_path = None
    try:
        suffix = Path(secure_filename(upload.filename)).suffix or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            upload.save(tmp_path)

        theme = generate_slack_theme(tmp_path, shuffle=shuffle)
        return jsonify({"theme": theme}), 200
    except Exception:  # pragma: no cover - defensive logging
        current_app.logger.exception("Failed to generate Slack theme from upload")
        return jsonify({"error": "failed to generate theme"}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                current_app.logger.warning("Unable to remove temp file: %s", tmp_path)
