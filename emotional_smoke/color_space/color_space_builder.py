import random
import sys

sys.path.append('/Users/devonperoutky/Development/processing/utilities')

from color_space import ColorSpace
from color_space_item import ColorSpaceItem
from color.color_diff import rgb2lab

class ColorSpaceBuilder(object):

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
    def build_color_space_from_image(img_pixels, size=None):
        i = 0
        lab_colors = []
        for pixel in img_pixels:
            i += 1
            rgb_color = (red(pixel), green(pixel), blue(pixel))
            lab_color = rgb2lab(rgb_color)
            tree_node = ColorSpaceItem(lab_data=lab_color, rgb_data=rgb_color)
            lab_colors.append(tree_node)
            if size and i > size:
                break
        return ColorSpace(lab_colors=lab_colors)
