import sys
import random

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/ds')

import kdtree
from color.color_diff import rgb2lab, cie94

class ColorSpace(object):
    def __init__(self, lab_colors):
        self.space = kdtree.create(lab_colors)
    
    def pop_most_similar_color(self, neighbors):
        cie94_colors = [rgb2lab((red(n.COLOR), green(n.COLOR), blue(n.COLOR))) for n in neighbors if n.COLOR]

        if not cie94_colors:
            return self.random_color()

        # CONVERT TO cie94 first??!?!?!?
        closest_neighbor_colors = [self.space.search_nn(neighbor_color, dist=cie94) for neighbor_color in cie94_colors]
        cleansed_colors = [color_distance_tuple for color_distance_tuple in closest_neighbor_colors if color_distance_tuple]
        if not cleansed_colors:
            return self.random_color()
        closest_neighbor_color = min(cleansed_colors, key = lambda t: t[1])
        closest_rgb_color = closest_neighbor_color[0].data.rgb_color
        self.space = self.space.remove(closest_neighbor_color[0].data)
        return color(closest_rgb_color[0], closest_rgb_color[1], closest_rgb_color[2])

    @staticmethod
    def random_color():
        return color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
