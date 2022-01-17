import sys
import time

sys.path.append('/Users/devonperoutky/Development/processing/utilities')
print(sys.path)

import random
from color.color_diff import calc_pixel_color_distance

class ColorSpace(object):
    def __init__(self):
        self.space = []
        self.used = set([])
    
    def add_color(self, color):
        self.space.append(color)

    def remove_color(self, color):
        self.space.remove(color)

    def pop_random_color(self):
        return self.space.pop()

    def pop_most_similar_color(self, neighbors):
        # random_index = random.randint(0, len(self.space) -1)
        # return self.space[random_index]

        print([str(n) for n in neighbors])
        colors = [n.COLOR for n in neighbors if n.COLOR]
        options = [c for c in self.space if c not in self.used]

        print(len(colors))
        if not colors:
            print("Poping a random color")
            return ColorSpaceExplorer.random_color()

        t1 = time.time()
        closest_color = None
        closest_distance = None
        for color_option in options:
            # color_distance = sum([calc_pixel_color_distance(color_option, node) for node in colors])
            color_distance = random.random()
            if not closest_color:
                closest_distance = color_distance
                closest_color = color_option
            else:
                if color_distance < closest_distance:
                    closest_distance = color_distance
                    closest_color = color_option

        t2 = time.time()
        print("Finding the nearest color took {}".format(t2 - t1))
        self.used.add(closest_color)
        return closest_color


class ColorSpaceBuilder(object):

    @staticmethod
    def build_RGB_color_space(size=None):
        color_space = ColorSpace()
        i = 0
        for red_value in range(0, 256):
            for green_value in range(0, 256):
                for blue_value in range(0, 256):
                    i += 1
                    color_space.add_color(color(red_value, green_value, blue_value))
                    if size and i >= size:
                        return color_space
        return color_space

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

    def __init__(self, color_space, height, width, starting_coord):
        self.color_space = color_space
        self.height = height
        self.width = width
        self.grid = [[Coordinate(x, y) for y in range(0, height - 1)] for x in range(0, width)]

        initial_coordiante = self.grid[starting_coord.X][starting_coord.Y]
        self.queue.append(initial_coordiante)
        self.visited.add(initial_coordiante)

    def BFS_iteration(self, iteration_amount):
        i = 0
        newly_colored_nodes = []
        while self.queue and i < iteration_amount:
            # Get the next coordinate and mark as visited
            coor = self.queue.pop(0)
            visited_neighbors, unvisited_neighbors = self.get_neighbors(coor)
            print("------------------")
            print("Visiting {}".format(str(coor)))
            print("Visited neighbors ({}): {}".format(len(visited_neighbors), [str(n) for n in visited_neighbors]))

            # TODO: Assign the color based on visited_neighbors
            assigned_color = self.calculate_color(visited_neighbors)
            print("Assigned color is ({}, {}, {})".format(red(assigned_color), green(assigned_color), blue(assigned_color)))
            coor.set_color(assigned_color)
            self.grid[coor.X][coor.Y] = coor
            newly_colored_nodes.append(coor)

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
        return Coordinate(random.randint(0, width - 1), random.randint(0, height - 1), ColorSpaceExplorer.random_color())



total_pixels_colored = 0
grid_height = 1000
grid_width = 1000
starting_coord = ColorSpaceExplorer.random_coordinate(grid_height, grid_width)
color_space = ColorSpaceBuilder.build_RGB_color_space(grid_height * grid_width)
print("COLOR SPACE has {} entries".format(len(color_space.space)))
color_space_explorer = ColorSpaceExplorer(color_space=color_space, height=grid_height, width=grid_width, starting_coord=starting_coord)


def setup():
    size(grid_height, grid_width)
    background(255, 255, 255)
    noStroke()
    frameRate(1)


def draw():
    global color_space_explorer, total_pixels_colored

    nodes_to_color = color_space_explorer.BFS_iteration(100)
    total_pixels_colored += len(nodes_to_color)
    for node in nodes_to_color:
        if node.COLOR:
            stroke(node.COLOR)
            point(node.X, node.Y)
    print("DRAWN")
