import unittest
import random
from gen_slack_theme import *


class TestGenSlackTheme(unittest.TestCase):

    def color_intensity(self):
        return random.randint(1, 256)

    def rgb_stub(self):
        return (
            self.color_intensity(),
            self.color_intensity(),
            self.color_intensity())

    def rgba_stub(self, a=None):
        if a is None:
            a = random.uniform(0, 1)
        return (
            self.color_intensity(),
            self.color_intensity(),
            self.color_intensity(),
            a)

    def test_upper(self):
        self.assertEqual(True, True)

    def test_theme_to_string(self):
        result = theme_to_string(['#fff', '#eee', '#000'])
        self.assertEqual(result, '#fff,#eee,#000')

    def test_retrieve_elligible_colors_default(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        pixels_count_color = [(9, pixel1), (100, pixel2), (11, pixel3)]

        result = retrieve_elligible_colors(pixels_count_color)
        self.assertEqual(list(result), [pixel2, pixel3])

    def test_retrieve_elligible_colors_different_pertinence(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        pixels_count_color = [(9, pixel1), (100, pixel2), (11, pixel3)]

        result = retrieve_elligible_colors(pixels_count_color, 99)
        self.assertEqual(result, [pixel2])

    def test_is_clear_returns_false_with_RGB(self):
        clear_color = self.rgb_stub()
        self.assertFalse(is_clear(clear_color))

    def test_is_clear_returns_false_with_RGBA(self):
        clear_color = self.rgba_stub(a=1)
        self.assertFalse(is_clear(clear_color))

    def test_is_clear_returns_true(self):
        clear_color = self.rgba_stub(a=0)
        self.assertTrue(is_clear(clear_color))

    def test_to_rgb_with_rgb(self):
        rgb_color = self.rgb_stub()
        self.assertEqual(to_rgb(rgb_color), rgb_color)

    def test_to_rgb_with_rgba(self):
        rgba_color = self.rgba_stub()
        r, g, b, _ = rgba_color
        self.assertEqual(to_rgb(rgba_color), (r, g, b))

    def test_complete_colors(self):
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        rgb_colors = [pixel1, pixel2, pixel3]
        white = "#ffffff"
        expected = [
            pixel1, pixel2, pixel3, white,
            pixel1, pixel2, pixel3, white,
            pixel1, pixel2, pixel3, white,
            pixel1, pixel2, pixel3, white, ]

        result = complete_colors(rgb_colors)
        self.assertEqual(result, expected)

    def test_complete_colors_enough_colors_already(self):
        pixel0 = self.rgb_stub()
        pixel1 = self.rgb_stub()
        pixel2 = self.rgb_stub()
        pixel3 = self.rgb_stub()
        pixel4 = self.rgb_stub()
        pixel5 = self.rgb_stub()
        pixel6 = self.rgb_stub()
        pixel7 = self.rgb_stub()
        pixel8 = self.rgb_stub()
        pixel9 = self.rgb_stub()
        rgb_colors = [
            pixel0, pixel1, pixel2, pixel3,
            pixel4, pixel5, pixel6, pixel7,
            pixel8, pixel9]

        result = complete_colors(rgb_colors)
        self.assertEqual(result, rgb_colors)

    def test_get_theme_more_than_picks(self):
        sut = list(range(0, 100))
        result = get_theme(sut, 10)
        self.assertEqual(len(result), 10)

    def test_get_theme_less_than_picks(self):
        sut = list(range(0, 5))
        result = get_theme(sut, 10)
        self.assertEqual(len(result), 5)

    def test_compute_colors_for_theme_no_shuffle(self):
        result = compute_colors_for_theme('test_image.png', False)
        expected = [
            '#eceaed', '#edebec', '#eeedeb', '#ededeb', '#ecebeb',
            '#ebebeb', '#eceaeb', '#ebe9eb', '#e6e7eb', '#edecea']
        self.assertEqual(result, expected)

    def test_compute_colors_for_theme_with_shuffle(self):
        result = compute_colors_for_theme('test_image.png', False)
        self.assertEqual(len(result), 10)
        self.assertTrue(type(result) is list)

    def test_generate_slack_theme_with_shuffle(self):
        result = generate_slack_theme('test_image.png', True)
        self.assertTrue(type(result) is str)

    def test_generate_slack_theme_no_shuffle(self):
        result = generate_slack_theme('test_image.png', False)
        expected = '#eceaed,#edebec,#eeedeb,#ededeb,#ecebeb,#ebebeb,#eceaeb,#ebe9eb,#e6e7eb,#edecea'
        self.assertEqual(result, expected)
