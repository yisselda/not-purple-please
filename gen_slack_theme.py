import unittest
from PIL import Image
import random

NB_SLACK_COLORS = 8
BLACK = "#000000"
WHITE = "#ffffff" 


def show():
    im = Image.open("test.png")
    pixels = im.getcolors()
    rgba_colors = [ color for count, color in pixels if valid_color(color) and count > 10 ]
    hex_colors = [ rgb2hex(r, g, b) for r, g, b, _ in rgba_colors ]
    theme = get_theme(hex_colors, dark_mode=True)
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

def gen_slack_theme(image):
    return ["#3F0E40","#350d36","#1164A3","#FFFFFF","#350D36","#FFFFFF","#2BAC76","#CD2553"]

class TestGenSlackTheme(unittest.TestCase):
    
    def test_gen_slack_theme(self):
        image = "url.png"
        result = gen_slack_theme(image)
        self.assertEqual(len(result), 8)

if __name__ == '__main__':
    print("YO, IT'S THE BEGINNING")
    show()
    print("YO, IT'S THE END")
    
    unittest.main()
