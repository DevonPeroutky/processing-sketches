import random
import sys
from coordinate import Coordinate

sys.path.append('/Users/devonperoutky/Development/processing/utilities')

from color.utils import random_rgb_color

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
    def random_coordinate(height, width):
        red = color(220, 40, 40)
        print("RED: {}".format(red))
        coor = Coordinate(10, 10, red)
        print(coor)
        return coor
        # random_x = random.randint(0, width - 1)
        # random_y = random.randint(0, height - 1)
        # print("RANDOM: ({}, {})".format(random_x, random_y))
        # return Coordinate(10, 10, red)
        # return Coordinate(random_x, random_y, red)
