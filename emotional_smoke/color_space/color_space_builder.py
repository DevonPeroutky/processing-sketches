import random
import sys

sys.path.append('/Users/devonperoutky/Development/processing/utilities')

from color_space import ColorSpace
from color_space_item import ColorSpaceItem
from color.color_diff import rgb2lab

class ColorSpaceBuilder(object):

    @staticmethod
    def gen_random_color_values():
        random_red = random.randint(0, 255)
        random_green = random.randint(0, 255)
        random_blue = random.randint(0, 255)
        return (random_red, random_green, random_blue)

    @staticmethod
    def build_full_RGB_color_space(size=None):
        rgb_colors = set()
        while(len(rgb_colors) < size):
            random_color = ColorSpaceBuilder.gen_random_color_values()
            rgb_colors.add(random_color)
        print("We have {} RGB colors ".format(len(rgb_colors)))

        space_items = [ColorSpaceItem(lab_data=rgb2lab(rgb_color), rgb_data=rgb_color) for rgb_color in rgb_colors]
        return ColorSpace(lab_colors=space_items)

    @staticmethod
    def build_RGB_color_space(size=None):
        i = 0
        lab_colors = []

        for red_value in range(0, 256):
            for green_value in range(0, 256):
                for blue_value in range(0, 256):
                    i += 1
                    rgb_color = (red_value, green_value, blue_value)
                    lab_color = rgb2lab(rgb_color)
                    tree_node = ColorSpaceItem(lab_data=lab_color, rgb_data=rgb_color)
                    lab_colors.append(tree_node)
                    if size and i >= size:
                        return ColorSpace(lab_colors=lab_colors)
        return ColorSpace(lab_colors=lab_colors)


    @staticmethod
    def build_color_space_from_image(img):
        pass
