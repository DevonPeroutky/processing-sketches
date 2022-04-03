import sys
import time

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
sys.path.append('/Users/devonperoutky/Development/processing/utilities/ds')

import random
import kdtree
from color.color_diff import calc_pixel_color_distance, rgb2lab, cie94

class ColorSpaceItem(object):
    def __init__(self, lab_data, rgb_data):
        self.lab_color = lab_data
        self.rgb_color = rgb_data

    def __len__(self):
        return len(self.lab_color)

    def __getitem__(self, i):
        return self.lab_color[i]

    def __repr__(self):
        return 'Item({}, {}, {}, {})'.format(self.lab_color[0], self.lab_color[1], self.lab_color[2], self.rgb_color)

class ColorSpace(object):
    def __init__(self, lab_colors):
        self.space = kdtree.create(lab_colors)
    
    def pop_most_similar_color(self, neighbors):
        cie94_colors = [rgb2lab((red(n.COLOR), green(n.COLOR), blue(n.COLOR))) for n in neighbors if n.COLOR]

        if not cie94_colors:
            return ColorSpaceExplorer.random_color()

        # CONVERT TO cie94 first??!?!?!?
        closest_neighbor_colors = [self.space.search_nn(neighbor_color, dist=cie94) for neighbor_color in cie94_colors]
        cleansed_colors = [color_distance_tuple for color_distance_tuple in closest_neighbor_colors if color_distance_tuple]
        if not cleansed_colors:
            return ColorSpaceExplorer.random_color()
        closest_neighbor_color = min(cleansed_colors, key = lambda t: t[1])
        closest_rgb_color = closest_neighbor_color[0].data.rgb_color
        self.space = self.space.remove(closest_neighbor_color[0].data)
        return color(closest_rgb_color[0], closest_rgb_color[1], closest_rgb_color[2])

class ColorSpaceBuilder(object):

    @staticmethod
    def build_RGB_color_space(size=None):
        i = 0
        lab_colors = []
        for red_value in range(100, 256):
            for green_value in range(100, 256):
                for blue_value in range(100, 256):
                    i += 1
                    rgb_color = (red_value, green_value, blue_value)
                    lab_color = rgb2lab(rgb_color)
                    tree_node = ColorSpaceItem(lab_data=lab_color, rgb_data=rgb_color)
                    lab_colors.append(tree_node)
                    if size and i >= size:
                        return ColorSpace(lab_colors=lab_colors)
        return ColorSpace(lab_colors=lab_colors)


    def build_color_space_from_image(self):
        pass

class Coordinate(object):

    def __init__(self, x, y, coor_color = None):
        self.X = x
        self.Y = y
        self.COLOR = coor_color

    def set_color(self, color):
        self.COLOR = color

    def __key(self):
        return (self.X, self.Y)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        if self.COLOR:
            return "({}, {}) --> ({}, {}, {})".format(self.X, self.Y, red(self.COLOR), green(self.COLOR), blue(self.COLOR))
        else:
            return "({}, {})".format(self.X, self.Y)

    def __hash__(self):
        return hash(self.__key())


class ColorSpaceExplorer(object):
    queue = []
    visited = set()

    def __init__(self, color_space, height, width, node_size, starting_coord):
        self.color_space = color_space
        self.height = height
        self.width = width
        self.grid = [[Coordinate(x, y) for y in range(0, height - 1, node_size)] for x in range(0, width, node_size)]

        initial_coordiante = self.grid[starting_coord.X][starting_coord.Y]
        self.queue.append(initial_coordiante)
        self.visited.add(initial_coordiante)

    def BFS_iteration(self, iteration_amount):
        i = 0
        newly_colored_nodes = [None] * iteration_amount
        while self.queue and i < iteration_amount:

            # Get the next coordinate and mark as visited
            coor = self.queue.pop(0)
            visited_neighbors, unvisited_neighbors = self.get_neighbors(coor)
            assigned_color = self.calculate_color(visited_neighbors)
            coor.set_color(assigned_color)
            self.grid[coor.X][coor.Y] = coor
            newly_colored_nodes[i] = coor

            # Traverse
            for neighbor in unvisited_neighbors:
                self.queue.append(neighbor)
                self.visited.add(neighbor)

            i += 1
        return newly_colored_nodes


    def calculate_color(self, neighbors):
        # return ColorSpaceExplorer.random_color()
        return self.color_space.pop_most_similar_color(neighbors)


    def _generate_valid_neighboring_coordinates(self, coordinate):
        coordinates = []
        for x in range(coordinate.X - 1, coordinate.X + 2):
            for y in range(coordinate.Y - 1, coordinate.Y + 2):
                if x > 0 and x < self.width and y > 0 and y < self.height and not (x == coordinate.X and y == coordinate.Y):
                    coordinates.append(self.grid[x][y])
        return coordinates


    def get_neighbors(self, coordinate):
        visited_neighbors, unvisited_neighbors = [], []
        all_neighbors = self._generate_valid_neighboring_coordinates(coordinate=coordinate) 
        for n in all_neighbors:
            (visited_neighbors if n in self.visited else unvisited_neighbors).append(n)

        return (visited_neighbors, unvisited_neighbors)


    @staticmethod
    def random_color():
        return color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def random_coordinate(height, width):
        red = color(220, 40, 40)
        return Coordinate(10, 10, red)
        # return Coordinate(random.randint(0, width - 1), random.randint(0, height - 1), red)
        # return Coordinate(random.randint(0, width - 1), random.randint(0, height - 1), ColorSpaceExplorer.random_color())



total_pixels_colored = 0
grid_height = 1000
grid_width = 1000
node_size = 1 # Don't change this
starting_coord = ColorSpaceExplorer.random_coordinate(grid_height, grid_width)
color_space = ColorSpaceBuilder.build_RGB_color_space(grid_height * grid_width)
color_space.space.rebalance()
print("COLOR SPACE has {} entries".format(len(list(color_space.space.inorder()))))
color_space_explorer = ColorSpaceExplorer(color_space=color_space, height=grid_height, width=grid_width, starting_coord=starting_coord, node_size=node_size)


def setup():
    # size(grid_height, grid_width)
    fullScreen()
    background(255, 255, 255)
    noStroke()
    frameRate(12)


def draw():
    global color_space_explorer, total_pixels_colored, node_size
    nodes_to_color = color_space_explorer.BFS_iteration(30)
    total_pixels_colored += len(nodes_to_color)
    for node in nodes_to_color:
        draw_point(node=node, node_size=node_size)
    print("DRAWN!")


def draw_point(node, node_size):
    fill(node.COLOR)
    square(node.X, node.Y, node_size)
