import io
import os
import unittest

from werkzeug.datastructures import FileStorage

from app.services.theme_service import InvalidThemeUpload, ThemeService, ThemeServiceError


class ThemeServiceTests(unittest.TestCase):
    def _file(self, *, name: str) -> FileStorage:
        return FileStorage(stream=io.BytesIO(b"fake-image-bytes"), filename=name)

    def test_generate_theme_returns_normalized_string_and_cleans_tempfile(self):
        captured = {}

        def stub_generator(path: str, shuffle: bool):
            captured["path"] = path
            captured["shuffle"] = shuffle
            self.assertTrue(os.path.exists(path))
            return ["#111111", "#222222"]

        service = ThemeService(generator=stub_generator, allowed_extensions={"png"})
        upload = self._file(name="sample.png")

        result = service.generate_theme(upload, shuffle=False)

        self.assertEqual(result, "#111111,#222222")
        self.assertIn("path", captured)
        self.assertFalse(os.path.exists(captured["path"]))
        self.assertFalse(captured["shuffle"])

    def test_generate_theme_rejects_missing_upload(self):
        service = ThemeService(generator=lambda *_: "#fff")
        with self.assertRaises(InvalidThemeUpload):
            service.generate_theme(None)  # type: ignore[arg-type]

    def test_generate_theme_rejects_empty_filename(self):
        service = ThemeService(generator=lambda *_: "#fff")
        with self.assertRaises(InvalidThemeUpload):
            service.generate_theme(self._file(name=""))

    def test_generate_theme_rejects_unsupported_extension(self):
        service = ThemeService(generator=lambda *_: "#fff")
        with self.assertRaises(InvalidThemeUpload):
            service.generate_theme(self._file(name="sample.bmp"))

    def test_generate_theme_wraps_generator_errors(self):
        def exploding_generator(*_):
            raise ValueError("boom")

        service = ThemeService(generator=exploding_generator)

        with self.assertRaises(ThemeServiceError):
            service.generate_theme(self._file(name="sample.png"))

