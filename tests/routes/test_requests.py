import io
import unittest

from app import create_app


class RequestApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        class StubThemeService:
            def __init__(self):
                self.invocations = []

            def generate_theme(self, upload, shuffle):
                self.invocations.append({"upload": upload, "shuffle": shuffle})
                return "#101010,#202020"

        self.stub_service = StubThemeService()
        self.app.extensions["theme_service"] = self.stub_service

    def test_create_theme_returns_generated_theme(self):
        response = self.client.post(
            "/v1/themes/create-theme",
            data={"file": (io.BytesIO(b"fake-bytes"), "sample.png")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"theme": "#101010,#202020"})
        self.assertEqual(len(self.stub_service.invocations), 1)
        invocation = self.stub_service.invocations[0]
        self.assertEqual(invocation["upload"].filename, "sample.png")
        self.assertTrue(invocation["shuffle"])

    def test_create_theme_missing_file_returns_400(self):
        response = self.client.post(
            "/v1/themes/create-theme",
            data={},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "missing file field"})
        self.assertFalse(self.stub_service.invocations)

    def test_health_returns_ok_status(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_health_rejects_post_method(self):
        response = self.client.post("/health")

        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
