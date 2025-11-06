import random
import unittest

from app.domain.slack_theme import core as gst


class TestSlackThemeCore(unittest.TestCase):
    def color_intensity(self):
        return random.randint(1, 256)

    def rgb_stub(self):
        return (self.color_intensity(), self.color_intensity(), self.color_intensity())

    def rgba_stub(self, a=None):
        if a is None:
            a = random.uniform(0, 1)
        return (
            self.color_intensity(),
            self.color_intensity(),
            self.color_intensity(),
            a,
        )

    def test_theme_to_string(self):
        result = gst.theme_to_string(["#fff", "#eee", "#000"])
        self.assertEqual(result, "#fff,#eee,#000")

    def test_retrieve_elligible_colors_default(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        pixels_count_color = [(9, pixel1), (100, pixel2), (11, pixel3)]

        result = gst.retrieve_elligible_colors(pixels_count_color)
        self.assertEqual(list(result), [pixel2, pixel3])

    def test_retrieve_elligible_colors_different_pertinence(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        pixels_count_color = [(9, pixel1), (100, pixel2), (11, pixel3)]

        result = gst.retrieve_elligible_colors(pixels_count_color, 99)
        self.assertEqual(result, [pixel2])

    def test_is_clear_returns_false_with_rgb(self):
        self.assertFalse(gst.is_clear(self.rgb_stub()))

    def test_is_clear_returns_false_with_rgba(self):
        self.assertFalse(gst.is_clear(self.rgba_stub(a=1)))

    def test_is_clear_returns_true(self):
        self.assertTrue(gst.is_clear(self.rgba_stub(a=0)))

    def test_to_rgb_with_rgb(self):
        rgb_color = self.rgb_stub()
        self.assertEqual(gst.to_rgb(rgb_color), rgb_color)

    def test_to_rgb_with_rgba(self):
        rgba_color = self.rgba_stub()
        r, g, b, _ = rgba_color
        self.assertEqual(gst.to_rgb(rgba_color), (r, g, b))

    def test_complete_colors(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        rgb_colors = [pixel1, pixel2, pixel3]
        white = "#ffffff"
        expected = [
            pixel1,
            pixel2,
            pixel3,
            white,
            pixel1,
            pixel2,
            pixel3,
            white,
            pixel1,
            pixel2,
            pixel3,
            white,
            pixel1,
            pixel2,
            pixel3,
            white,
        ]

        result = gst.complete_colors(rgb_colors)
        self.assertEqual(result, expected)

    def test_complete_colors_enough_colors_already(self):
        rgb_colors = [self.rgb_stub() for _ in range(10)]
        self.assertEqual(gst.complete_colors(rgb_colors.copy()), rgb_colors)

    def test_get_theme_more_than_picks(self):
        sut = list(range(0, 100))
        result = gst.get_theme(sut, 10)
        self.assertEqual(len(result), 10)

    def test_get_theme_less_than_picks(self):
        sut = list(range(0, 5))
        result = gst.get_theme(sut, 10)
        self.assertEqual(len(result), 5)

    def test_compute_colors_for_theme_no_shuffle(self):
        result = gst.compute_colors_for_theme("test_image.png", False)
        expected = [
            "#eceaed",
            "#edebec",
            "#eeedeb",
            "#ededeb",
            "#ecebeb",
            "#ebebeb",
            "#eceaeb",
            "#ebe9eb",
            "#e6e7eb",
            "#edecea",
        ]
        self.assertEqual(result, expected)

    def test_compute_colors_for_theme_with_shuffle(self):
        result = gst.compute_colors_for_theme("test_image.png", False)
        self.assertEqual(len(result), 10)
        self.assertIsInstance(result, list)

    def test_generate_slack_theme_with_shuffle(self):
        result = gst.generate_slack_theme("test_image.png", True)
        self.assertIsInstance(result, str)

    def test_generate_slack_theme_no_shuffle(self):
        result = gst.generate_slack_theme("test_image.png", False)
        expected = (
            "#eceaed,#edebec,#eeedeb,#ededeb,#ecebeb,"
            "#ebebeb,#eceaeb,#ebe9eb,#e6e7eb,#edecea"
        )
        self.assertEqual(result, expected)

    def test_rgb2hex_formats_expected_string(self):
        self.assertEqual(gst.rgb2hex(26, 43, 60), "#1a2b3c")
