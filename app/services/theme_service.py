from __future__ import annotations

import contextlib
import logging
import os
from collections.abc import Sequence
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, Iterable

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ThemeGenerator = Callable[[str, bool], Sequence[str] | str]


class ThemeServiceError(RuntimeError):
    """Raised when theme creation fails for unexpected reasons."""


class InvalidThemeUpload(ThemeServiceError):
    """Raised when the uploaded file cannot be processed."""


class ThemeService:
    def __init__(
        self,
        *,
        generator: ThemeGenerator,
        allowed_extensions: Iterable[str] | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._generator = generator
        allowed = allowed_extensions or {"png", "jpg", "jpeg", "gif"}
        self._allowed_extensions = {ext.lower().lstrip(".") for ext in allowed}
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    def generate_theme(self, upload: FileStorage, *, shuffle: bool = True) -> str:
        if upload is None:
            raise InvalidThemeUpload("missing file field")

        filename = secure_filename(upload.filename or "")
        if not filename:
            raise InvalidThemeUpload("empty filename")

        extension = Path(filename).suffix.lstrip(".").lower()
        if not extension or extension not in self._allowed_extensions:
            raise InvalidThemeUpload("unsupported file type")

        suffix = f".{extension}"
        try:
            with self._temporary_file(suffix) as tmp_path:
                upload.save(tmp_path)
                theme = self._generator(tmp_path, shuffle=shuffle)
                return self._normalize_theme(theme)
        except InvalidThemeUpload:
            raise
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.exception("Theme generation failed")
            raise ThemeServiceError("failed to generate theme") from exc

    def _normalize_theme(self, theme: Sequence[str] | str) -> str:
        if isinstance(theme, str):
            return theme
        return ",".join(theme)

    @contextlib.contextmanager
    def _temporary_file(self, suffix: str):
        tmp = NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            tmp.close()
            yield tmp.name
        finally:
            try:
                os.remove(tmp.name)
            except FileNotFoundError:
                return
            except OSError:  # pragma: no cover - defensive logging
                self._logger.warning("Unable to remove temporary file: %s", tmp.name)
