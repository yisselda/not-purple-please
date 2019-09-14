import random
import sys
import unittest

from PIL import Image


NB_SLACK_COLORS = 8
BLACK = "#000000"
WHITE = "#ffffff"

# Order
# Column BG, Menu BG Hover, Active Item, Active Item Text, Hover Item, Text Color, Active Presence, Mention Badge
# Column BG <> Text Color <> Hover Item
# Column BG <> Active Item
# Column BG <> Active Presence
# Column BG <> Mention Badge
# Active Item <> Active Item Text

def generate_slack_theme(filepath):
    im = Image.open(filepath)
    pixels = im.getcolors()
    rgba_colors = [ color for count, color in pixels if valid_color(color) and count > 10 ]
    hex_colors = [ rgb2hex(r, g, b) for r, g, b, _ in rgba_colors ]
    theme = get_theme(hex_colors)
    print(theme_to_string(theme))

def theme_to_string(theme):
    return ','.join(theme)

def get_theme(hex, dark_mode=False):
    number_colors = len(hex)
    if number_colors < NB_SLACK_COLORS:
        if number_colors < NB_SLACK_COLORS / 2:
            extra_color = BLACK if dark_mode else WHITE 
            hex.append(extra_color)
        
        repeat = NB_SLACK_COLORS // number_colors + 1
        hex *= repeat
    return pick_wisely(hex, NB_SLACK_COLORS)

def pick_wisely(collection_list, number_of_picks):
    random.shuffle(collection_list)
    return collection_list[:number_of_picks]
    
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def valid_color(color):
    r, g, b, a = color
    return  a > 0

if __name__ == '__main__':
    doc = """
------------------------------------------------------------------

This script generates a slack theme based on an image's colors.

Run the following command:
$ python3 gen_slack_theme.py <image-path>

------------------------------------------------------------------
    """
    if len(sys.argv) < 2:
        print(doc)
    else:
        filepath = sys.argv[1]
        generate_slack_theme(filepath)
