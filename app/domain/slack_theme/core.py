import random

from PIL import Image

NB_SLACK_COLORS = 10
BLACK = "#000000"
WHITE = "#ffffff"

# Order
# Column BG, Menu BG Hover, Active Item, Active Item Text,
# Hover Item, Text Color, Active Presence, Mention Badge
# Column BG <> Text Color
# Column BG <> Hover Item
# Text Color <> Hover Item
# Column BG <> Active Item
# Active Item <> Active Item Text
# Column BG <> Active Presence
# Column BG <> Mention Badge


def generate_slack_theme(filepath, shuffle=True):
    colors_for_theme = compute_colors_for_theme(filepath, shuffle)
    return theme_to_string(colors_for_theme)


def compute_colors_for_theme(filepath, shuffle=True):
    image = Image.open(filepath)
    if image.mode == "P":
        # Palette PNGs (like logos) need explicit conversion to preserve transparency.
        image = image.convert("RGBA")
    image = image.convert("RGB")
    pixels = image.getcolors(99999999)

    rgb_colors = retrieve_elligible_colors(pixels)

    # TODO order by the most important ones and cut to less than 100
    more_colors = complete_colors(rgb_colors)

    rgb_theme = get_theme(more_colors, NB_SLACK_COLORS, shuffle)

    return [rgb2hex(r, g, b) for r, g, b in rgb_theme]


def theme_to_string(theme):
    return ",".join(theme)


def to_rgb(color):
    if len(color) == 3:
        return color

    if len(color) == 4:
        r, g, b, _ = color
        return (r, g, b)


def retrieve_elligible_colors(pixels_count_color, pertinent_colors_nb=10):
    return [
        to_rgb(color)
        for count, color in pixels_count_color
        if count > pertinent_colors_nb and not is_clear(color)
    ]


def complete_colors(colors, dark_mode=False):
    number_colors = len(colors)
    if number_colors < NB_SLACK_COLORS:
        if number_colors < NB_SLACK_COLORS / 2:
            extra_color = BLACK if dark_mode else WHITE
            colors.append(extra_color)

        repeat = NB_SLACK_COLORS // number_colors + 1
        colors *= repeat
    return colors


def get_theme(colors, number_of_picks, shuffle=False):
    colors_list = list(colors)
    if shuffle:
        random.shuffle(colors_list)
    return colors_list[:number_of_picks]


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def is_clear(color):
    if len(color) < 4:
        return False

    if len(color) == 4:
        _, _, _, a = color
        return a == 0

    return False
