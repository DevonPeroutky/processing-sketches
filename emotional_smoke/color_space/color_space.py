import sys
import random

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/ds')

import kdtree
from color.color_diff import rgb2lab, cie94
from color.utils import random_rgb_color

class ColorSpace(object):
    def __init__(self, lab_colors):
        self.space = kdtree.create(lab_colors)

    def pop_most_similar_color_optimized(self, neighbors, threshold = .25):
        cie94_colors = [rgb2lab((n.RED_VALUE, n.GREEN_VALUE, n.BLUE_VALUE)) for n in neighbors if n.COLOR]
        if not cie94_colors:
            return random_rgb_color()

        # CONVERT TO cie94 first??!?!?!?
        closest_neighbor = None
        closest_distance = None
        for neighbor_color in cie94_colors:
            (color_item, distance) = self.space.search_nn(neighbor_color, dist=cie94) or (None, None)

            if not color_item or not distance:
                print(self.space)
                if (len(list(self.space.inorder())) == 0):
                    print("SPACE HAs RUN OUT. Rebalancing!")
                    self.space.rebalance()
                    if (len(list(self.space.inorder())) == 0):
                        print("SPACE HAs RUN OUT. Rebalancing!")
                        raise Exception("Color Space has run out!")
                return random_rgb_color()


            # If below threshold, return immediately
            if distance < threshold:
                closest_neighbor_color = color_item.data.rgb_color
                print("Found something below the threshold! {} -> {}".format(closest_neighbor_color, distance))
                self.space = self.space.remove(color_item.data)
                return color(closest_neighbor_color[0], closest_neighbor_color[1], closest_neighbor_color[2])


            if closest_distance is None or distance < closest_distance:
                closest_neighbor = color_item.data
                closest_distance = distance

        if closest_neighbor:
            closest_neighbor_color = closest_neighbor.rgb_color
            print("Returning color {}".format(closest_neighbor_color))
            self.space.remove(closest_neighbor)
            return color(closest_neighbor_color[0], closest_neighbor_color[1], closest_neighbor_color[2])
        else:
            print("THIS SHOULD NOT BE CALLED A LOT")
            random_rgb_color()

    def pop_most_similar_color(self, neighbors):
        cie94_colors = [rgb2lab((n.RED_VALUE, n.GREEN_VALUE, n.BLUE_VALUE)) for n in neighbors if n.COLOR]

        # print("CIE94: {}".format(cie94_colors))

        if not cie94_colors:
            return random_rgb_color()

        # CONVERT TO cie94 first??!?!?!?
        closest_neighbor_colors = [self.space.search_nn(neighbor_color, dist=cie94) for neighbor_color in cie94_colors]
        # print(closest_neighbor_colors)
        cleansed_colors = [color_distance_tuple for color_distance_tuple in closest_neighbor_colors if color_distance_tuple]
        if not cleansed_colors:
            return random_rgb_color()
        closest_neighbor_color = min(cleansed_colors, key = lambda t: t[1])
        closest_rgb_color = closest_neighbor_color[0].data.rgb_color
        self.space = self.space.remove(closest_neighbor_color[0].data)
        return color(closest_rgb_color[0], closest_rgb_color[1], closest_rgb_color[2])
